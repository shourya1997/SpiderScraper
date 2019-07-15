<html>
  <head>
      <title>Form Example</title>
  </head>
  <body>
    <form method="post" action="/submit">
        <fieldset>
            <legend>SAMPLE FORM</legend>
            <ul>
                <li>Website URLs (for multiple websites put ',' in between. eg:www.google.com,www.facebook.com) <input name='website_urls'>
                </li>
            </ul><input type='submit' value='Submit Form'>
        </fieldset>
    </form>

    <p>{{message}}</p>

  </body>
</html>