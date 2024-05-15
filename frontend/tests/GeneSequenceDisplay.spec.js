import { shallowMount } from '@vue/test-utils';
import GeneSequenceDisplay from '@/components/GeneSequenceDisplay.vue';

describe('GeneSequenceDisplay.vue', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(GeneSequenceDisplay);
    expect(wrapper.find('h1').text()).toBe('Gene Sequence Display');
    expect(wrapper.find('input').exists()).toBe(true);
    expect(wrapper.find('button').exists()).toBe(true);
    expect(wrapper.find('textarea').exists()).toBe(true);
  });

  it('fetches the gene sequence when the button is clicked', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ seq: 'ATCG' }),
      })
    );

    const wrapper = shallowMount(GeneSequenceDisplay);
    wrapper.setData({ geneId: 'ENSG000001' });

    await wrapper.find('button').trigger('click');
    expect(global.fetch).toHaveBeenCalledWith('http://rest.ensembl.org/sequence/id/ENSG000001', expect.any(Object));
    expect(wrapper.vm.gene_seq_content).toBe('ATCG');

    global.fetch.mockClear();
  });
});
