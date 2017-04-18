
gapi.load('auth2', function() {
  auth2 = gapi.auth2.init({
    client_id: '1050453128023-lpuo4af45992ivtcf80jqq4gpghka0l0.apps.googleusercontent.com',
    // Scopes to request in addition to 'profile' and 'email'
    //scope: 'additional_scope'
  });
});

$('#gsignin').click(function() {
  // signInCallback defined in step 6.
  auth2.grantOfflineAccess().then(signInCallback);
});

function signInCallback(authResult) {
  if (authResult['code']) {
    // Hide the sign-in button now that the user is authorized
    $('#gsignin').attr('style', 'display: none');
    // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
    $.ajax({
      type: 'POST',
      url: '/gconnect',
      // Always include an `X-Requested-With` header in every AJAX request,
      // to protect against CSRF attacks.
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      processData: false,
      data: authResult['code'],
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        // Handle or verify the server response if necessary.
        //alert('Succesfully logged in!');
        window.location.href = '/';
      },
      error: function(result) {
        alert('Failed to make a server-side call. Check your configuration and console.');
      }
    });
  }
}

function googleLogout() {
  $.ajax({
    type: 'POST',
    url: '/logout',
    // Always include an `X-Requested-With` header in every AJAX request,
    // to protect against CSRF attacks.
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    },
    processData: false,
    contentType: 'application/octet-stream; charset=utf-8',
    success: function(result) {
      // Handle or verify the server response if necessary.
      auth2.disconnect();
      alert('Succesfully logged out!');
      window.location.href = '/';
    },
    error: function(result) {
      alert('Failed to make a server-side call. Check your configuration and console.');
    }
  });
}

function setDialogCallback(callbackText) {
  $('#delete-dialog button[name=delete]').attr('onclick', callbackText);
}

function deleteFailure() {
  alert('You are not the owner of this item and do not have authorization to delete!');
}

function closeDeleteDialog() {
  $('#delete-dialog').modal('hide');
}

function deleteCatalog(catalogID) {
  $.ajax({
    type: 'POST',
    url: '/deletecatalog/' + catalogID,
    success: closeDeleteDialog,
    error: deleteFailure
  });
}

function deleteCategory(catalogID, categoryID) {
  $.ajax({
    type: 'POST',
    url: '/catalog/' + catalogID + "/deletecategory/" + categoryID,
    success: closeDeleteDialog,
    error: deleteFailure
  });
}

function deleteItem(catalogID, itemID) {
  $.ajax({
    type: 'POST',
    url: '/catalog/' + catalogID + "/deleteitem/" + itemID,
    success: closeDeleteDialog,
    error: deleteFailure
  });
}



$(window).resize(function() {
  $('.catalog-picture').height($('.catalog-picture').width());
  $('.item-picture').height($('.item-picture').width());
});
$(window).resize();
