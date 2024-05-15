import { shallowMount } from '@vue/test-utils';
import HomePage from '@/pages/HomePage.vue';
import HomeComp from '@/components/HomeComp.vue';

describe('HomePage.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(HomePage);
    expect(wrapper.findAllComponents(HomeComp).length).toBe(2);
  });
});
