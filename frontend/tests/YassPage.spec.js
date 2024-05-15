import { shallowMount } from '@vue/test-utils';
import YassPage from '@/pages/YassPage.vue';
import RunYass from '@/components/RunYass.vue';

describe('YassPage.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(YassPage);
    expect(wrapper.findComponent(RunYass).exists()).toBe(true);
  });
});
