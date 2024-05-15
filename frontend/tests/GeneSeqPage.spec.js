import { shallowMount } from '@vue/test-utils';
import GeneSeqPage from '@/pages/GeneSeqPage.vue';
import GeneSequenceDisplay from '@/components/GeneSequenceDisplay.vue';

describe('GeneSeqPage.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(GeneSeqPage);
    expect(wrapper.findComponent(GeneSequenceDisplay).exists()).toBe(true);
  });
});
