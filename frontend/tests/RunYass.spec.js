import { shallowMount } from '@vue/test-utils';
import RunYass from '@/components/RunYass.vue';
import Plotly from 'plotly.js-dist';

jest.mock('plotly.js-dist', () => ({
  newPlot: jest.fn(),
  react: jest.fn(),
  relayout: jest.fn(),
  redraw: jest.fn(),
  purge: jest.fn(),
  toImage: jest.fn().mockResolvedValue('mocked-image'),
}));

jest.mock('@/assets/camera.png', () => 'test-file-stub');

const mockVisualizationData = {
  dotplot_data: {
    data: [
      {
        marker: {},
        mode: 'markers',
        name: 'Forward',
        type: 'scattergl',
        x: [1, 2, 3],
        y: [4, 5, 6],
      },
      {
        marker: {},
        mode: 'markers',
        name: 'Reverse',
        type: 'scattergl',
        x: [7, 8, 9],
        y: [10, 11, 12],
      }
    ],
    layout: {
      height: 550,
      width: 780,
      title: { text: 'Dot Plot of Gene Similarities' },
      xaxis: { nticks: 10, range: [0, 10], showgrid: false, title: { text: 'X Axis' } },
      yaxis: { nticks: 10, range: [0, 15], showgrid: false, title: { text: 'Y Axis' } }
    }
  },
  gene_structure1_plot: {
    data: [
      { fill: 'tozeroy', fillcolor: 'black', mode: 'lines', opacity: 0.6, x: [1, 2, 3], y: [4, 5, 6] },
      { mode: 'lines', opacity: 0.6, x: [7, 8, 9], y: [10, 11, 12] }
    ],
    layout: {
      height: 90,
      width: 780,
      xaxis: { range: [0, 10], showgrid: false },
      yaxis: { range: [0, 15], showgrid: false }
    }
  },
  gene_structure2_plot: {
    data: [
      { fill: 'tozeroy', fillcolor: 'black', mode: 'lines', opacity: 0.6, x: [1, 2, 3], y: [4, 5, 6] },
      { mode: 'lines', opacity: 0.6, x: [7, 8, 9], y: [10, 11, 12] }
    ],
    layout: {
      height: 90,
      width: 550,
      xaxis: { range: [0, 10], showgrid: false, tickangle: -90 },
      yaxis: { range: [0, 15], showgrid: false }
    }
  },
  exon_intervals1: {
    ENSMMUT00000058138: [[42, 404], [1176, 1241], [2685, 2877], [3496, 4357]],
    ENSMMUT00000067524: [[42, 85], [857, 922], [2366, 2558], [3177, 3210], [3619, 3878]]
  },
  exon_intervals2: {
    ENST00000335295: [[10, 151], [282, 504], [1355, 1617]],
    ENST00000380315: [[100, 200], [300, 400], [500, 600]],
  },
  data_for_manual_zoom: {
    directions: [['forward', 'r'], ['reverse', 'f']],
    min_x: 0,
    max_x: 10,
    min_y: 0,
    max_y: 15,
    inverted: false,
    sampling_fraction: '0.1',
    x_label: 'Gene1',
    y_label: 'Gene2'
  }
};

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
      },
      data() {
        return {
          visualizations: mockVisualizationData, // Ensure visualizations are set
          manualZoom: { x1: null, x2: null, y1: null, y2: null } // Initialize with default values
        };
      }
    });
  });

  it('renders the component', () => {
    expect(wrapper.exists()).toBe(true);
  });

  it('updates GeneID1 and GeneID2 when input changes', async () => {
    const textareas = wrapper.findAll('textarea');
    const geneID1Input = textareas.at(0);
    const geneID2Input = textareas.at(1);
  
    geneID1Input.setValue('ENSG00000139618');
    geneID2Input.setValue('ENSG00000157764');
  
    await wrapper.vm.$nextTick();
  
    expect(wrapper.vm.GeneID1).toBe('ENSG00000139618');
    expect(wrapper.vm.GeneID2).toBe('ENSG00000157764');
  });

  it('calls runEvoGenes method on button click', async () => {
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
    expect(wrapper.vm.errorMessage).toBe("Please provide two Valid Ensembl Gene IDs.");
  });

  it('shows loader when loading is true', async () => {
    wrapper.setData({ loading: true });
    await wrapper.vm.$nextTick();
    expect(wrapper.findComponent({ name: 'LoaderOverlay' }).props().visible).toBe(true);
  });

  it('renders error message when errorMessage is set', async () => {
    wrapper.setData({ errorMessage: 'An error occurred' });
    await wrapper.vm.$nextTick();
    expect(wrapper.find('.error-message').text()).toBe('An error occurred');
  });


  
  
  
  

  it('renders visualizations when data is available', async () => {
    wrapper.setData({
      visualizations: mockVisualizationData
    });
    await wrapper.vm.$nextTick();
    expect(wrapper.find('.visualization-container').exists()).toBe(true);
  });

  it('calls applyManualZoom method on manual zoom button click', async () => {
    wrapper.vm.applyManualZoom = jest.fn();
    wrapper.setData({
      visualizations: mockVisualizationData // Mocking visualizations to ensure the button is rendered
    });
    await wrapper.vm.$nextTick();
    wrapper.find('#apply-zoom-button').trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.applyManualZoom).toHaveBeenCalled();
  });

  it('calls clearInputs method when clearInputs is called', async () => {
    wrapper.vm.clearInputs();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.GeneID1).toBe('');
    expect(wrapper.vm.GeneID2).toBe('');
  });

  it('updates manual zoom inputs correctly', async () => {
    const zoomInputs = wrapper.findAll('.zoom-input');
    
    // Ensure we have the expected number of inputs
    expect(zoomInputs.length).toBe(4);
  
    zoomInputs.at(0).setValue(2);
    zoomInputs.at(1).setValue(8);
    zoomInputs.at(2).setValue(4);
    zoomInputs.at(3).setValue(10);
    
    await wrapper.vm.$nextTick();
    
    expect(wrapper.vm.manualZoom.x1).toBe(2);
    expect(wrapper.vm.manualZoom.x2).toBe(8);
    expect(wrapper.vm.manualZoom.y1).toBe(4);
    expect(wrapper.vm.manualZoom.y2).toBe(10);
  });
  
  it('updates sampling fraction when selection changes', async () => {
    const select = wrapper.find('#sampling-fraction-select');
    select.setValue('0.01');
    
    await wrapper.vm.$nextTick();
    
    expect(wrapper.vm.selectedSamplingFraction).toBe('0.01');
  });
    // Test visibility of loader overlay
    it('shows loader overlay when loading', async () => {
      wrapper.setData({ loading: true });
      await wrapper.vm.$nextTick();
      
      const loaderOverlay = wrapper.findComponent({ name: 'LoaderOverlay' });
      expect(loaderOverlay.props().visible).toBe(true);
    });
  
    // Test visibility of modal window
    it('displays modal when showModal is true', async () => {
      wrapper.setData({ showModal: true });
      await wrapper.vm.$nextTick();
      
      const modal = wrapper.find('.modal-overlay');
      expect(modal.exists()).toBe(true);
    });
  
    // Test error message display on invalid manual zoom input
    it('displays error message on invalid manual zoom input', async () => {
      wrapper.setData({
        manualZoom: { x1: 10, x2: 2, y1: null, y2: null },
        visualizations: mockVisualizationData
      });
      
      await wrapper.vm.applyManualZoom();
      await wrapper.vm.$nextTick();
      
      expect(wrapper.vm.ZoomErrorMessage).toBe("Invalid zoom coordinates: x1 should be less than x2 and y1 should be less than y2");
    });
  
    // Test capturing screenshot
    it('calls captureScreenshot method on export button click', async () => {
      wrapper.vm.captureScreenshot = jest.fn();
      wrapper.setData({ visualizations: mockVisualizationData });
      
      await wrapper.vm.$nextTick();
      wrapper.find('.export-button img').trigger('click');
      
      expect(wrapper.vm.captureScreenshot).toHaveBeenCalled();
    });
    
    // Test if the correct parent option is selected
    it('updates selectedParent1 and selectedParent2 when option changes', async () => {
      wrapper.setData({ visualizations: mockVisualizationData });
  
      await wrapper.vm.$nextTick();
      
      const parentSelect1 = wrapper.find('#parent-select1');
      const parentSelect2 = wrapper.find('#parent-select2');
      
      parentSelect1.setValue('ENSMMUT00000067524');
      parentSelect2.setValue('ENST00000380315');
      
      await wrapper.vm.$nextTick();
      
      expect(wrapper.vm.selectedParent1).toBe('ENSMMUT00000067524');
      expect(wrapper.vm.selectedParent2).toBe('ENST00000380315');
    });
    it('matches snapshot when loading', () => {
      wrapper.setData({ loading: true });
      expect(wrapper.html()).toMatchSnapshot();
    });
    it('displays error message with correct class when error occurs', async () => {
      wrapper.setData({ errorMessage: 'An error occurred' });
      await wrapper.vm.$nextTick();
      
      const errorMessage = wrapper.find('.error-message');
      expect(errorMessage.classes()).toContain('error-message');
    });
    
  
    
    
    it('displays manual zoom input fields correctly', async () => {
      wrapper.setData({
        manualZoom: { x1: 1, x2: 5, y1: 2, y2: 6 }
      });
      await wrapper.vm.$nextTick();
    
      const zoomInput = wrapper.find('.zoom-input-pair');
      expect(zoomInput.exists()).toBe(true);
    });
    it('handles non-200 response correctly', async () => {
      // Mock the fetchWithProgress method to simulate a non-200 response
      wrapper.vm.fetchWithProgress = jest.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ message: 'Please Provide Valid Ensembl Gene ID' })
      });
    
      wrapper.setData({
        GeneID1: 'ENSG00000139618',
        GeneID2: 'ENSG00000157764'
      });
    
      await wrapper.vm.runEvoGenes();
    
      expect(wrapper.vm.errorMessage).toBe('Please Provide Valid Ensembl Gene ID');
      expect(wrapper.vm.loading).toBe(false);
      expect(wrapper.vm.isRunning).toBe(true);
    });
    
    
    
    
    
    it('handles incomplete data from server', async () => {
      // Mock the fetchWithProgress method to simulate incomplete data response
      wrapper.vm.fetchWithProgress = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ exon_intervals1: null, exon_intervals2: null })
      });
    
      wrapper.setData({
        GeneID1: 'ENSG00000139618',
        GeneID2: 'ENSG00000157764'
      });
    
      await wrapper.vm.runEvoGenes();
    
      expect(wrapper.vm.errorMessage).toBe('Please Provide Valid Ensembl Gene ID');
      expect(wrapper.vm.loading).toBe(false);
      expect(wrapper.vm.isRunning).toBe(true);
    });
    
    
    
    
    
  
    it('handles missing Gene IDs', async () => {
      wrapper.setData({
        GeneID1: '',
        GeneID2: ''
      });
    
      await wrapper.vm.runEvoGenes();
    
      expect(wrapper.vm.errorMessage).toBe('Please provide two Valid Ensembl Gene IDs.');
      expect(wrapper.vm.loading).toBe(false);
      expect(wrapper.vm.isRunning).toBe(true);
    });
    
    
    

    it('handles successful response and renders plots', async () => {
      // Mock the fetchWithProgress method to simulate a successful response
      wrapper.vm.fetchWithProgress = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => mockVisualizationData
      });
    
      wrapper.setData({
        GeneID1: 'ENSG00000139618',
        GeneID2: 'ENSG00000157764'
      });
    
      await wrapper.vm.runEvoGenes();
    
      expect(wrapper.vm.visualizations.gene_structure1_plot).toEqual(mockVisualizationData.gene_structure1_plot);
      expect(wrapper.vm.visualizations.gene_structure2_plot).toEqual(mockVisualizationData.gene_structure2_plot);
      expect(wrapper.vm.$refs.dotplot).toBeDefined();
      expect(wrapper.vm.$refs.geneStructure1).toBeDefined();
      expect(wrapper.vm.$refs.geneStructure2).toBeDefined();
    });

    it('updates gene structures correctly based on selected parent', () => {
      wrapper.setData({
        selectedParent1: 'ENSMMUT00000058138',
        visualizations: mockVisualizationData
      });
      
      wrapper.vm.updateGeneStructure('geneStructure1', wrapper.vm.selectedParent1);
      
      expect(wrapper.vm.visualizations.gene_structure1_plot).toEqual(mockVisualizationData.gene_structure1_plot);
    });
    it('handles partial data response gracefully', async () => {
      wrapper.vm.fetchWithProgress = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ gene_structure1_plot: null })
      });
      
      await wrapper.vm.runEvoGenes();
      
      expect(wrapper.vm.errorMessage).toBe('Please provide two Valid Ensembl Gene IDs.');
    });
    it('does not allow invalid Gene IDs to be submitted', async () => {
      wrapper.setData({
        GeneID1: 'InvalidID',
        GeneID2: 'InvalidID'
      });
      
      await wrapper.vm.runEvoGenes();
      
      expect(wrapper.vm.errorMessage).toBe('Please Provide Valid Ensembl Gene ID');
    });
    it('reacts to changes in selectedSamplingFraction', async () => {
      wrapper.setData({ selectedSamplingFraction: '0.05' });
      await wrapper.vm.$nextTick();
      
      expect(wrapper.vm.selectedSamplingFraction).toBe('0.05');
    });
    it('emits custom event when process completes', async () => {
      wrapper.vm.$emit('process-completed', { status: 'success' });
      await wrapper.vm.$nextTick();
      
      expect(wrapper.emitted('process-completed')).toBeTruthy();
      expect(wrapper.emitted('process-completed')[0]).toEqual([{ status: 'success' }]);
    });

    it('handles edge cases in applyManualZoom correctly', async () => {
      wrapper.setData({
        manualZoom: { x1: 100, x2: 2, y1: -5, y2: 10000 },
        visualizations: mockVisualizationData
      });
      
      await wrapper.vm.applyManualZoom();
      
      expect(wrapper.vm.ZoomErrorMessage).toBe("Invalid zoom coordinates: x1 should be less than x2 and y1 should be less than y2");
    });

  
    
    it('shows and hides modal correctly', async () => {
      wrapper.setData({ showModal: true });
      await wrapper.vm.$nextTick();
      expect(wrapper.find('.modal-overlay').isVisible()).toBe(true);
    
      await wrapper.find('.modal-overlay').trigger('click');
      expect(wrapper.vm.showModal).toBe(false);
    });
    it('renders error message div when errorMessage is set', async () => {
      wrapper.setData({ errorMessage: 'An error occurred' });
      await wrapper.vm.$nextTick();
      expect(wrapper.find('.error-message').exists()).toBe(true);
    });

  
    
});
