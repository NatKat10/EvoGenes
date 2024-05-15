import { shallowMount } from '@vue/test-utils';
import About from '@/components/About.vue';

describe('About.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(About);
    expect(wrapper.exists()).toBe(true);
  });

  it('renders the correct number of items', () => {
    const wrapper = shallowMount(About);
    const items = wrapper.findAll('.slider-item');
    expect(items.length).toBe(wrapper.vm.items.length);
  });

  it('renders the correct content for each item', () => {
    const wrapper = shallowMount(About);
    const items = wrapper.vm.items;

    items.forEach((item, index) => {
      const sliderItem = wrapper.findAll('.slider-item').at(index);
      expect(sliderItem.find('img').attributes('src')).toBe(item.imageUrl);
      expect(sliderItem.find('h3').text()).toBe(item.title);
      expect(sliderItem.find('p').text()).toBe(item.description);
      expect(sliderItem.find('a').attributes('href')).toBe(item.link);
      expect(sliderItem.find('a').text()).toBe(item.buttonLabel);
    });
  });
});
