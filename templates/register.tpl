    <div class="container">
        <div class="row">
            <div class="panel panel-default login-form">
                <div class="panel-body">
                    <form>
                        <div class="err-msg hidden">
                            <div class="alert alert-danger" role="alert">
                                <p>登録に失敗しました</p>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="Username" class="control-label">Username</label>
                            <input type="text" class="form-control" id="Username" placeholder="Username" required>
                        </div>
                        <div class="form-group">
                            <label for="Password" class="control-label">Password</label>
                            <input type="password" class="form-control" id="Password" placeholder="Password" required>
                        </div>
                        <input type="button" class="btn btn-default UserRegistSubmit" value="Submit">
                    </form>
                </div>
                <!--/panel-body -->
            </div>
            <!--/panel -->
            <div class="panel panel-default RegisterCompleted hidden">
                <div class="panel-body">
                    <h3>Registration Completed!</h3>
                        <button class="btn btn-default go2cpanel">Go to Control Panel</button>
                </div>
                <!--/panel-body -->
            </div>
            <!--/panel -->

        </div>
    </div>
    <!-- /.container -->
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="<TMPL_VAR NAME="PATH_PREFIX">bootstrap/js/bootstrap.min.js"></script>
    <script src="<TMPL_VAR NAME="PATH_PREFIX">script.js"></script>
    <script src="<TMPL_VAR NAME="PATH_PREFIX">jquery.cookie.js"></script>
</body>

</html>
