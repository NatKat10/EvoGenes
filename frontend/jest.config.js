module.exports = {
    moduleFileExtensions: ['js', 'json', 'vue'],
    transform: {
      '^.+\\.vue$': 'vue-jest',
      '^.+\\.js$': 'babel-jest',
      '^.+\\.(css|scss|png|jpg|svg)$': '<rootDir>/jest.setup.js',
    },
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1'
    },
    testMatch: ['**/tests/**/*.spec.js'],
    collectCoverage: true,
    collectCoverageFrom: ['**/*.{js,vue}', '!**/node_modules/**']
  };
  