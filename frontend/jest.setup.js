// jest.setup.js
module.exports = {
    process() {
      return 'module.exports = {};';
    },
    getCacheKey() {
      return 'staticAsset';
    },
  };


//   to run the tests paste "npm run test" in the terminal from frontend directory
