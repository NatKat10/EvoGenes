import { shallowMount } from '@vue/test-utils';
import appNavbar from '@/components/appNavbar.vue';

describe('appNavbar.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(appNavbar, {
      stubs: ['router-link'],
    });
    expect(wrapper.find('.sidebar').exists()).toBe(true);
    expect(wrapper.find('.logo img').exists()).toBe(true);
    expect(wrapper.findAll('.nav-link').length).toBe(5); // Adjust the number based on the actual links
  });

  it('opens and closes the sidebar on mouse enter and leave', async () => {
    const wrapper = shallowMount(appNavbar, {
      stubs: ['router-link'],
    });
    const sidebar = wrapper.find('.sidebar');

    await sidebar.trigger('mouseenter');
    expect(wrapper.vm.isOpen).toBe(true);

    await sidebar.trigger('mouseleave');
    expect(wrapper.vm.isOpen).toBe(false);
  });
});
