
<!DOCTYPE html>

<html>
<head>
  <meta charset='utf-8'>
  <meta http-equiv="X-UA-Compatible" content="chrome=1">
  <title>${title}</title>
  <meta name="description" content="${description}">
  <meta name="author" content="Nicolas Vanhoren">

  <link rel="stylesheet" type="text/css" href="./bootstrap.min.css" />

</head>
<body>

  <div class="container">
    <div class="row">
      <div class="col-md-8 col-md-push-2">
        <%block name="content">
        </%block>
      </div>
    </div>
  </div>

</body>
</html>
