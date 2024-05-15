import { shallowMount } from '@vue/test-utils';
import GeneInput from '@/components/GeneInput.vue';

describe('GeneInput.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(GeneInput);
    expect(wrapper.find('h1').text()).toBe('Gene Input Page hiiiiiiiiii');
    expect(wrapper.find('textarea#gene1').exists()).toBe(true);
    expect(wrapper.find('textarea#gene2').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it('submits the form correctly', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ message: 'Graph generated' }),
      })
    );

    const wrapper = shallowMount(GeneInput);
    wrapper.setData({ gene1: 'ATCG', gene2: 'CGTA' });

    await wrapper.find('form').trigger('submit.prevent');

    expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/generate', expect.objectContaining({
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gene_name: 'user_input', sequence1: 'ATCG', sequence2: 'CGTA' }),
    }));

    global.fetch.mockClear();
  });
});