const { JSDOM } = require('jsdom');
const { Canvas, Image, ImageData } = require('canvas');

const dom = new JSDOM();
global.window = dom.window;
global.document = dom.window.document;
global.navigator = dom.window.navigator;

global.HTMLCanvasElement = dom.window.HTMLCanvasElement;
global.HTMLImageElement = dom.window.HTMLImageElement;
global.Image = Image;
global.ImageData = ImageData;
global.Blob = dom.window.Blob;
global.URL = dom.window.URL;

// Mock createObjectURL
global.URL.createObjectURL = jest.fn();

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
  })
);

// Mock alert
global.window.alert = jest.fn();


//   to run the tests paste "npm run test" in the terminal from frontend directory
