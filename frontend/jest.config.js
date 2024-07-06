module.exports = {
  moduleFileExtensions: ['js', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': 'vue-jest',
    '^.+\\.js$': 'babel-jest',
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(jpg|jpeg|png|gif|svg|png)$': '<rootDir>/__mocks__/fileMock.js',
  },
  testMatch: ['**/tests/**/*.spec.js'],
  collectCoverage: true,
  collectCoverageFrom: ['src/components/RunYass.vue'],
  setupFiles: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jsdom',
  transformIgnorePatterns: [
    '/node_modules/',
    '<rootDir>/src/assets/',
  ],
};
