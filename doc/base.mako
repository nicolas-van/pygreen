
<!DOCTYPE html>

<html>
<head>
  <meta charset='utf-8'>
  <meta http-equiv="X-UA-Compatible" content="chrome=1">
  <title>${self.attr.title}</title>
  <meta name="description" content="${self.attr.description}">
  <meta name="author" content="Nicolas Vanhoren">

  <link rel="stylesheet" type="text/css" href="./index.css" />

</head>
<body>

  <a href="https://github.com/nicolas-van/pygreen"><img style="position: absolute; top: 0; right: 0; border: 0;"
    src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>

  <div class="container">
    <div class="row">
      <div class="col-md-12 py-5">
        ${self.body()}
      </div>
    </div>
  </div>

</body>
</html>
