import * as TypeaheadSpec from '../../ui/composite/TypeaheadSpec';
import * as TypeaheadSchema from '../../ui/schema/TypeaheadSchema';
import { TypeaheadSketcher } from '../../ui/types/TypeaheadTypes';
import * as Sketcher from './Sketcher';

const Typeahead = Sketcher.composite({
  name: 'Typeahead',
  configFields: TypeaheadSchema.schema(),
  partFields: TypeaheadSchema.parts(),
  factory: TypeaheadSpec.make
}) as TypeaheadSketcher;

export {
  Typeahead
};
