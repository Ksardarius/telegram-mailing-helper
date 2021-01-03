<!DOCTYPE html>
<html style="font-size: 16px;">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <meta name="keywords" content="Рассылки: админка">
    <meta name="description" content="">
    <meta name="page_type" content="np-template-header-footer-from-plugin">
    <title>users</title>
    <link rel="stylesheet" href="nicepage.css" media="screen">
<link rel="stylesheet" href="users.css" media="screen">
    <script class="u-script" type="text/javascript" src="jquery-1.9.1.min.js" defer=""></script>
    <script class="u-script" type="text/javascript" src="nicepage.js" defer=""></script>
    <meta name="generator" content="Nicepage 3.3.5, nicepage.com">
    <link id="u-theme-google-font" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,400i,500,500i,700,700i,900,900i|Open+Sans:300,300i,400,400i,600,600i,700,700i,800,800i">


    <script type="application/ld+json">{
		"@context": "http://schema.org",
		"@type": "Organization",
		"name": "",
		"url": "index.html"
}</script>
    <meta property="og:title" content="users">
    <meta property="og:type" content="website">
    <meta name="theme-color" content="#478ac9">
    <link rel="canonical" href="index.html">
    <meta property="og:url" content="index.html">
  </head>
  <body class="u-body"><header class="u-clearfix u-header u-header" id="sec-e980"><div class="u-clearfix u-sheet u-valign-middle u-sheet-1">
        <nav class="u-menu u-menu-dropdown u-offcanvas u-menu-1">
          <div class="menu-collapse" style="font-size: 1rem; letter-spacing: 0px;">
            <a class="u-button-style u-custom-left-right-menu-spacing u-custom-padding-bottom u-custom-top-bottom-menu-spacing u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="#">
              <svg><use xlink:href="#menu-hamburger"></use></svg>
              <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><symbol id="menu-hamburger" viewBox="0 0 16 16" style="width: 16px; height: 16px;"><rect y="1" width="16" height="2"></rect><rect y="7" width="16" height="2"></rect><rect y="13" width="16" height="2"></rect>
</symbol>
</defs></svg>
            </a>
          </div>
          <div class="u-custom-menu u-nav-container">
            <ul class="u-nav u-unstyled u-nav-1"><li class="u-nav-item"><a class="u-button-style u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="users.html" style="padding: 10px 20px;">Пользователи</a>
</li><li class="u-nav-item"><a class="u-button-style u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="dispatch_lists.html" style="padding: 10px 20px;">Редактирование списков</a>
</li></ul>
          </div>
          <div class="u-custom-menu u-nav-container-collapse">
            <div class="u-black u-container-style u-inner-container-layout u-opacity u-opacity-95 u-sidenav">
              <div class="u-sidenav-overflow">
                <div class="u-menu-close"></div>
                <ul class="u-align-center u-nav u-popupmenu-items u-unstyled u-nav-2"><li class="u-nav-item"><a class="u-button-style u-nav-link" href="users.html" style="padding: 10px 20px;">Пользователи</a>
</li><li class="u-nav-item"><a class="u-button-style u-nav-link" href="dispatch_lists.html" style="padding: 10px 20px;">Редактирование списков</a>
</li></ul>
              </div>
            </div>
            <div class="u-black u-menu-overlay u-opacity u-opacity-70"></div>
          </div>
        </nav>
        <h1 class="u-text u-text-1">Рассылки: админка</h1>
      </div></header>
    <section class="u-align-center u-clearfix u-section-1" id="sec-2267">
      <div class="u-clearfix u-sheet u-valign-middle u-sheet-1">
        <div class="u-expanded-width u-table u-table-responsive u-table-1">
          <table class="u-table-entity u-table-entity-1">
            <colgroup>
              <col width="4%">
              <col width="24%">
              <col width="24%">
              <col width="24%">
              <col width="24%">
            </colgroup>
            <thead class="u-black u-table-header u-table-header-1">
              <tr style="height: 21px;">
                <th class="u-border-1 u-border-black u-table-cell">#ID</th>
                <th class="u-border-1 u-border-black u-table-cell">Пользователь</th>
                <th class="u-border-1 u-border-black u-table-cell">Состояние</th>
                <th class="u-border-1 u-border-black u-table-cell">Действия</th>
                <th class="u-border-1 u-border-black u-table-cell">Добавлен</th>
              </tr>
            </thead>
            <tbody class="u-table-alt-grey-5 u-table-body">
            % for user in users:
              <tr style="height: 78px;">
                <td class="u-border-1 u-border-grey-30 u-first-column u-grey-50 u-table-cell u-table-cell-5">{{user.id}}</td>
                <td class="u-border-1 u-border-grey-30 u-first-column u-grey-50 u-table-cell u-table-cell-5">{{user.name}}</td>
                <td class="u-border-1 u-border-grey-30 u-table-cell">{{userStateCls(user.state).getLocalizedMessage()}}</td>
                <td class="u-border-1 u-border-active-palette-2-base u-border-hover-palette-1-base u-btn-rectangle u-none u-table-cell u-text-palette-1-base u-table-cell-7">
                  <a href="#" onclick="{{'confirm' if user.state=='new' or user.state=='blocked' else 'block'}}('{{user.id}}')" class="u-active-none u-border-none u-btn u-button-link u-button-style u-hover-none u-none u-text-palette-1-base u-btn-1">Изменить состояние</a>
                </td>
                <td class="u-border-1 u-border-grey-30 u-table-cell">{{user.created}}</td>
              </tr>
            % end
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <script lang="js">
        function confirm(id){
            $.ajax({
                type: "POST",
                url: "/api/users/confirm",
                data: JSON.stringify({"id": id}),
                success: function(data){
                    document.location = "users.html"
                },
                contentType:"application/json; charset=utf-8",
                dataType:"json"
            });
        }
        function block(id){
            $.ajax({
                type: "POST",
                url: "/api/users/block",
                data: JSON.stringify({"id": id}),
                success: function(data){
                    document.location = "users.html"
                },
                contentType:"application/json; charset=utf-8",
                dataType:"json"
            });
        }
    </script>

    <footer class="u-align-center u-clearfix u-footer u-grey-80 u-footer" id="sec-f73b"><div class="u-clearfix u-sheet u-sheet-1">
      </div></footer>
  </body>
</html>