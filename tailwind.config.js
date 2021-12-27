module.exports = {
   mode: 'jit',
   purge: ['../**/templates/**/*.html'],
   darkMode: false,
   theme: {
      extend: {
         fontFamily: {
            'main': ['Roboto', 'sans-serif']
         },
         colors: {
            'primary': '#4338ca',
            'primary-darker': '#3730a3'
         }
      }
   },
   variants: {
      extend: {},
   },
   plugins: [],
}
