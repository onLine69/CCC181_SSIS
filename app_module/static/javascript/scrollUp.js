/** 
 * This is for the scroll up button found in the base.html.
*/

// Get the button
var mybutton = document.getElementById("scrollToTopBtn");

window.onscroll = () => {
    // When the user scrolls down 20px from the top of the document, show the button
    mybutton.style.display = (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) ?  "block" : "none";
}

// When the user clicks on the button, scroll to the top of the document
mybutton.onclick = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}