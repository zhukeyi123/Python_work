name: Documents
desc: Documents

tiles:
  - name: Documents
    interval: 43200

http:
  mitm:
    - "license.pdfexpert.com"
  script:
    - match: ^https:\/\/license\.pdfexpert\.com\/api\/2\.0\/documents\/subscription\/refresh
      name: license.pdfexpert.com
      type: response # request / response
      require-body: true
      timeout: 20
      argument: ''
      binary-mode: false
      max-size: 1048576 # 1MB
 
script-providers:
  Documents:
    url: https://raw.githubusercontent.com/Yu9191/Rewrite/main/Documents.js
    interval: 86400
