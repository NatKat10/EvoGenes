import { shallowMount } from '@vue/test-utils';
import HomeComp from '@/components/HomeComp.vue';

describe('HomeComp.vue', () => {
  it('renders the component correctly with props', () => {
    const wrapper = shallowMount(HomeComp, {
      propsData: {
        imageUrl: 'http://example.com/image.png',
        title: 'Home Component Title',
        description: 'Description of the Home Component',
        link: 'http://example.com',
        buttonLabel: 'Click Here',
      },
    });

    expect(wrapper.find('.card-title').text()).toBe('Home Component Title');
    expect(wrapper.find('.card-text').text()).toBe('Description of the Home Component');
    expect(wrapper.find('.btn').text()).toBe('Click Here');
    expect(wrapper.find('img').attributes('src')).toBe('http://example.com/image.png');
    expect(wrapper.find('.btn').attributes('href')).toBe('http://example.com');
  });
});
