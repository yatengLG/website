import { Arr, Fun, Result } from '@ephox/katamari';
import { Compare, Element, Focus, Node, Remove, Traverse } from '@ephox/sugar';

import { SugarEvent } from '../../alien/TypeDefinitions';
import { AlloyComponent } from '../../api/component/ComponentApi';
import * as Debugging from '../../debugging/Debugging';
import * as DescribedHandler from '../../events/DescribedHandler';
import * as GuiEvents from '../../events/GuiEvents';
import { FocusingEvent } from '../../events/SimulatedEvent';
import * as Triggers from '../../events/Triggers';
import Registry from '../../registry/Registry';
import * as Tagger from '../../registry/Tagger';
import * as GuiFactory from '../component/GuiFactory';
import * as SystemEvents from '../events/SystemEvents';
import { Container } from '../ui/Container';
import * as Attachment from './Attachment';
import { AlloySystemApi } from './SystemApi';

export interface GuiSystem {
  root: () => AlloyComponent;
  element: () => Element;
  destroy: () => void;
  add: (component: AlloyComponent) => void;
  remove: (component: AlloyComponent) => void;
  getByUid: (uid: string) => Result<AlloyComponent, string | Error>;
  getByDom: (element: Element) => Result<AlloyComponent, string | Error>;

  addToWorld: (comp: AlloyComponent) => void;
  removeFromWorld: (comp: AlloyComponent) => void;

  broadcast: (message: message) => void;
  broadcastOn: (channels: string[], message: message) => void;

  // TODO FIXME this is no longer tested directly
  broadcastEvent: (eventName: string, event: SugarEvent) => void;
}

export type message = Record<string, any>;

const create = (): GuiSystem => {
  const root = GuiFactory.build(
    Container.sketch({
      dom: {
        tag: 'div'
      }
    })
  );
  return takeover(root);
};

const takeover = (root: AlloyComponent): GuiSystem => {
  const isAboveRoot = (el: Element): boolean => {
    return Traverse.parent(root.element()).fold(
      () => {
        return true;
      },
      (parent) => {
        return Compare.eq(el, parent);
      }
    );
  };

  const registry = Registry();

  const lookup = (eventName: string, target: Element) => {
    return registry.find(isAboveRoot, eventName, target);
  };

  const domEvents = GuiEvents.setup(root.element(), {
    triggerEvent (eventName: string, event: SugarEvent) {
      return Debugging.monitorEvent(eventName, event.target(), (logger) => {
        return Triggers.triggerUntilStopped(lookup, eventName, event, logger);
      });
    },
  });

  const systemApi: AlloySystemApi = {
    // This is a real system
    debugInfo: Fun.constant('real'),
    triggerEvent (eventName: string, target: Element, data: any) {
      Debugging.monitorEvent(eventName, target, (logger) => {
        // The return value is not used because this is a fake event.
        Triggers.triggerOnUntilStopped(lookup, eventName, data, target, logger);
      });
    },
    triggerFocus (target: Element, originator: Element) {
      Tagger.read(target).fold(() => {
        // When the target is not within the alloy system, dispatch a normal focus event.
        Focus.focus(target);
      }, (_alloyId) => {
        Debugging.monitorEvent(SystemEvents.focus(), target, (logger) => {
          // NOTE: This will stop at first handler.
          Triggers.triggerHandler<FocusingEvent>(lookup, SystemEvents.focus(), {
            // originator is used by the default events to ensure that focus doesn't
            // get called infinitely
            originator: Fun.constant(originator),
            kill: Fun.noop,
            prevent: Fun.noop,
            target: Fun.constant(target)
          }, target, logger);
        });
      });
    },

    triggerEscape (comp, simulatedEvent) {
      systemApi.triggerEvent('keydown', comp.element(), simulatedEvent.event());
    },

    getByUid (uid) {
      return getByUid(uid);
    },
    getByDom (elem) {
      return getByDom(elem);
    },
    build: GuiFactory.build,
    addToGui (c) { add(c); },
    removeFromGui (c) { remove(c); },
    addToWorld (c) { addToWorld(c); },
    removeFromWorld (c) { removeFromWorld(c); },
    broadcast (message) {
      broadcast(message);
    },
    broadcastOn (channels, message) {
      broadcastOn(channels, message);
    },
    broadcastEvent (eventName: string, event: SugarEvent) {
      broadcastEvent(eventName, event);
    },
    isConnected: Fun.constant(true)
  };

  const addToWorld = (component) => {
    component.connect(systemApi);
    if (!Node.isText(component.element())) {
      registry.register(component);
      Arr.each(component.components(), addToWorld);
      systemApi.triggerEvent(SystemEvents.systemInit(), component.element(), { target: Fun.constant(component.element()) });
    }
  };

  const removeFromWorld = (component) => {
    if (!Node.isText(component.element())) {
      Arr.each(component.components(), removeFromWorld);
      registry.unregister(component);
    }
    component.disconnect();
  };

  const add = (component) => {
    Attachment.attach(root, component);
  };

  const remove = (component) => {
    Attachment.detach(component);
  };

  const destroy = () => {
    // INVESTIGATE: something with registry?
    domEvents.unbind();
    Remove.remove(root.element());
  };

  const broadcastData = (data) => {
    const receivers = registry.filter(SystemEvents.receive());
    Arr.each(receivers, (receiver) => {
      const descHandler = receiver.descHandler();
      const handler = DescribedHandler.getCurried(descHandler);
      handler(data);
    });
  };

  const broadcast = (message) => {
    broadcastData({
      universal: Fun.constant(true),
      data: Fun.constant(message)
    });
  };

  const broadcastOn = (channels, message) => {
    broadcastData({
      universal: Fun.constant(false),
      channels: Fun.constant(channels),
      data: Fun.constant(message)
    });
  };

  // This doesn't follow usual DOM bubbling. It will just dispatch on all
  // targets that have the event. It is the general case of the more specialised
  // "message". "messages" may actually just go away. This is used for things
  // like window scroll.
  const broadcastEvent = (eventName: string, event: SugarEvent) => {
    const listeners = registry.filter(eventName);
    return Triggers.broadcast(listeners, event);
  };

  const getByUid = (uid) => {
    return registry.getById(uid).fold(() => {
      return Result.error(
        new Error('Could not find component with uid: "' + uid + '" in system.')
      );
    }, Result.value);
  };

  const getByDom = (elem: Element): Result<AlloyComponent, any> => {
    const uid = Tagger.read(elem).getOr('not found');
    return getByUid(uid);
  };

  addToWorld(root);

  return {
    root: Fun.constant(root),
    element: root.element,
    destroy,
    add,
    remove,
    getByUid,
    getByDom,

    addToWorld,
    removeFromWorld,

    broadcast,
    broadcastOn,

    broadcastEvent
  };
};

export {
  create,
  takeover
};