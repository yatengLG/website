import { Log, Pipeline } from '@ephox/agar';
import { Editor } from '@ephox/mcagar';
import ImagePlugin from 'tinymce/plugins/image/Plugin';
import SilverTheme from 'tinymce/themes/silver/Theme';

import {
  cAssertCleanHtml,
  cExecCommand,
  cFillActiveDialog,
  cSubmitDialog,
  cWaitForDialog,
  silverSettings,
} from '../../module/Helpers';
import { UnitTest } from '@ephox/bedrock';

UnitTest.asynctest('Image dialog image_dimensions: false', (success, failure) => {
  SilverTheme();
  ImagePlugin();
  Pipeline.async({}, [
    Log.chainsAsStep('TBA', 'Image: image dialog image_dimensions: false', [
      Editor.cFromSettings({
        ...silverSettings,
        image_dimensions: false
      }),
      cExecCommand('mceImage', true),
      cWaitForDialog(),
      cFillActiveDialog({
        src: {
          value: 'src'
        },
        alt: 'alt'
      }),
      cSubmitDialog(),
      cAssertCleanHtml('Checking output', '<p><img src="src" alt="alt" /></p>'),
      Editor.cRemove
    ])
  ], () => success(), failure);
});
