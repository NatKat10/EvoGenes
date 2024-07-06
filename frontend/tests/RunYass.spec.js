import { shallowMount } from '@vue/test-utils';
import RunYass from '@/components/RunYass.vue';

// Mock the camera.png import to prevent issues
jest.mock('@/assets/camera.png', () => 'test-file-stub');

// Mock the $route object
const $route = {
  params: {
    comparison_id: '12345'
  }
};

describe('RunYass.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(RunYass, {
      stubs: {
        LoaderOverlay: true
      },
      mocks: {
        $route
      }
    });
  });

  it('renders the component', () => {
    expect(wrapper.exists()).toBe(true);
  });

  it('updates GeneID1 and GeneID2 when input changes', async () => {
    const geneID1Input = wrapper.find('textarea[placeholder="Enter Gene ID 1 here"]');
    const geneID2Input = wrapper.find('textarea[placeholder="Enter Gene ID 2 here"]');

    geneID1Input.setValue('ENSG00000139618');
    geneID2Input.setValue('ENSG00000157764');

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.GeneID1).toBe('ENSG00000139618');
    expect(wrapper.vm.GeneID2).toBe('ENSG00000157764');
  });

  it('calls runEvoGenes method on button click', async () => {
    // Manually bind the method to ensure it's available
    wrapper.vm.runEvoGenes = jest.fn();
    wrapper.setData({
      GeneID1: 'ENSG00000139618',
      GeneID2: 'ENSG00000157764'
    });
    wrapper.find('.btn button').trigger('click');

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.runEvoGenes).toHaveBeenCalled();
  });

  it('displays an error message if no input is provided', async () => {
    wrapper.vm.runEvoGenes();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.errorMessage).toBe("Please provide two sequences or two FASTA files or two Ensembl Gene IDs.");
  });

});
