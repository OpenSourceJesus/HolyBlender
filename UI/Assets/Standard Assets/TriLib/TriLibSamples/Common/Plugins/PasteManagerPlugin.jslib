var PasteManagerPlugin = {
  PasteManagerSetup: function() {
    document.body.addEventListener("paste", function(e) {
		e.preventDefault();
		var text = (e.originalEvent || e).clipboardData.getData('text/plain');
		SendMessage("PasteManager", "Paste", text);	
	});
  }
};
mergeInto(LibraryManager.library, PasteManagerPlugin);