http:
  script:
    - match: license.pdfexpert.com
      name: license.pdfexpert.com
      type: response # request / response
      require-body: true
      timeout: 20
      argument: ''
      binary-mode: false
      max-size: 1048576 # 1MB
 
script-providers:
  your-fancy-script:
    url: https://raw.githubusercontent.com/Yu9191/Rewrite/main/Documents.js
    interval: 86400
