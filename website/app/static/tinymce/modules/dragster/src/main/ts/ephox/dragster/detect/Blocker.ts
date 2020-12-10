import { Merger } from '@ephox/katamari';
import { Attr, Class, Css, Element, Remove } from '@ephox/sugar';
import Styles from '../style/Styles';

export interface BlockerOptions {
  layerClass: string;
}

export interface Blocker {
  element: () => Element;
  destroy: () => void;
}

export const Blocker = function (options: Partial<BlockerOptions>): Blocker {
  const settings: BlockerOptions = Merger.merge({
    layerClass: Styles.resolve('blocker')
  }, options);

  const div = Element.fromTag('div');
  Attr.set(div, 'role', 'presentation');
  Css.setAll(div, {
    position: 'fixed',
    left: '0px',
    top: '0px',
    width: '100%',
    height: '100%'
  });

  Class.add(div, Styles.resolve('blocker'));
  Class.add(div, settings.layerClass);

  const element = function () {
    return div;
  };

  const destroy = function () {
    Remove.remove(div);
  };

  return {
    element,
    destroy
  };
};