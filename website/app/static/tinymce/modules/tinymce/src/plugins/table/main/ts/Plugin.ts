/**
 * Copyright (c) Tiny Technologies, Inc. All rights reserved.
 * Licensed under the LGPL or a commercial license.
 * For LGPL see License.txt in the project root for license information.
 * For commercial licenses see https://www.tiny.cloud/
 */

import { Cell, Option } from '@ephox/katamari';
import { KeyboardEvent } from '@ephox/dom-globals';
import Editor from 'tinymce/core/api/Editor';
import PluginManager from 'tinymce/core/api/PluginManager';
import Clipboard from './actions/Clipboard';
import { TableActions } from './actions/TableActions';
import Commands from './api/Commands';
import { getResizeHandler } from './actions/ResizeHandler';
import TabContext from './queries/TabContext';
import CellSelection from './selection/CellSelection';
import Ephemera from './selection/Ephemera';
import { Selections } from './selection/Selections';
import { getSelectionTargets } from './selection/SelectionTargets';
import Buttons from './ui/Buttons';
import MenuItems from './ui/MenuItems';
import { hasTabNavigation } from './api/Settings';
import { getApi } from './api/Api';
import { Element } from '@ephox/sugar';

function Plugin(editor: Editor) {
  const selections = Selections(editor);
  const selectionTargets = getSelectionTargets(editor, selections);
  const resizeHandler = getResizeHandler(editor);
  const cellSelection = CellSelection(editor, resizeHandler.lazyResize, selectionTargets);
  const actions = TableActions(editor, resizeHandler.lazyWire);
  const clipboardRows = Cell(Option.none<Element<any>[]>());

  Commands.registerCommands(editor, actions, cellSelection, selections, clipboardRows);
  Clipboard.registerEvents(editor, selections, actions, cellSelection);

  MenuItems.addMenuItems(editor, selectionTargets);
  Buttons.addButtons(editor, selectionTargets);
  Buttons.addToolbars(editor);

  editor.on('PreInit', function () {
    editor.serializer.addTempAttr(Ephemera.firstSelected());
    editor.serializer.addTempAttr(Ephemera.lastSelected());
  });

  if (hasTabNavigation(editor)) {
    editor.on('keydown', function (e: KeyboardEvent) {
      TabContext.handle(e, editor, actions, resizeHandler.lazyWire);
    });
  }

  editor.on('remove', function () {
    resizeHandler.destroy();
    cellSelection.destroy();
  });

  return getApi(editor, clipboardRows, resizeHandler, selectionTargets);
}

export default function () {
  PluginManager.add('table', Plugin);
}
