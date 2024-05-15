import { shallowMount } from '@vue/test-utils';
import GeneStructure from '@/components/GeneStructure.vue';

describe('GeneStructure.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(GeneStructure);
    expect(wrapper.find('h1').text()).toBe('Gene Structure');
    expect(wrapper.find('form').exists()).toBe(true);
    expect(wrapper.find('input').exists()).toBe(true);
    expect(wrapper.find('button').exists()).toBe(true);
  });

  it('fetches and processes the gene structure', async () => {
    const mockData = [{ gene_id: 'ENSG000001', start: 100, end: 200 }];
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockData),
      })
    );

    const wrapper = shallowMount(GeneStructure);
    wrapper.setData({ geneId: 'ENSG000001' });

    await wrapper.find('form').trigger('submit.prevent');
    expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/generate/gene-structure', expect.any(Object));
    await wrapper.vm.$nextTick(); // Ensure data processing happens
    expect(wrapper.vm.geneStructure).toEqual(mockData);
    expect(wrapper.vm.exonsPositions).toEqual([[100, 200]]);

    global.fetch.mockClear();
  });
});
