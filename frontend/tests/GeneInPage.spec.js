import { shallowMount } from '@vue/test-utils';
import GeneInPage from '@/pages/GeneInPage.vue';

describe('GeneInPage.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(GeneInPage);
    expect(wrapper.exists()).toBe(true);
  });
});
