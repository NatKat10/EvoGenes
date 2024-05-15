// jest.setup.js
module.exports = {
    process() {
      return 'module.exports = {};';
    },
    getCacheKey() {
      return 'staticAsset';
    },
  };