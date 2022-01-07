module.exports = {
   mode: 'jit',
   purge: ['../**/templates/**/*.html'],
   darkMode: false,
   theme: {
      extend: {
         fontFamily: {
            'main': ['Roboto', 'sans-serif'],
            'logo': ['Oswald', 'sans-serif']
         },
         colors: {
            'primary': '#4338ca',
            'primary-brighter': '#6358ea',
            'primary-darker': '#3730a3',
            'primary-disabled': '#9790b3',
            'background': '#e2e8f0',
            'error': '#dc2626',
            'warning': '#facc15',
            'accept': '#1ebd10'
         },
         keyframes: {
            "slide-from-left": {
               '0%': { opacity: 0, transform: 'translateX(-12rem)' },
               '100%': { opacity: 1, transform: 'translateX(0)' },
            }
         },
         animation: {
            'slide-right': 'slide-from-left 0.4s linear'
         },
         boxShadow: {
            'inner-xl': 'inset 2px 2px 10px 2px rgba(0,0,0, 0.5)'
         },
      }
   },
   variants: {
      extend: {},
   },
   plugins: [],
}
