const passwordInput = document.getElementById("passwordField");
const strengthBar = document.getElementById("strengthBar");
const strengthText = document.getElementById("strengthText");
const charCount = document.getElementById("charCount");
const submitBtn = document.getElementById("submitBtn");
const reqLength = document.getElementById("req-length");
const reqLower = document.getElementById("req-lower");
const reqUpper = document.getElementById("req-upper");
const reqNumber = document.getElementById("req-number");

passwordInput.addEventListener("input", function() {
    let pw = this.value;
    let score = 0;
    if (pw.length >= 8) score += 25;
    if (/[a-z]/.test(pw)) score += 25;
    if (/[A-Z]/.test(pw)) score += 25;
    if (/[0-9]/.test(pw)) score += 25;
    
    reqLength.innerHTML = pw.length >= 8 ? '<i class="fas fa-check text-green-500"></i> 8+ characters' : '<i class="fas fa-circle text-xs"></i> 8+ characters';
    reqLower.innerHTML = /[a-z]/.test(pw) ? '<i class="fas fa-check text-green-500"></i> Lowercase' : '<i class="fas fa-circle text-xs"></i> Lowercase';
    reqUpper.innerHTML = /[A-Z]/.test(pw) ? '<i class="fas fa-check text-green-500"></i> Uppercase' : '<i class="fas fa-circle text-xs"></i> Uppercase';
    reqNumber.innerHTML = /[0-9]/.test(pw) ? '<i class="fas fa-check text-green-500"></i> Number' : '<i class="fas fa-circle text-xs"></i> Number';
    
    let color = "bg-red-500";
    let text = "Weak";
    if (score >= 50) { color = "bg-yellow-500"; text = "Medium"; }
    if (score >= 75) { color = "bg-green-500"; text = "Strong"; }
    if (score === 100) { color = "bg-green-400"; text = "Very Strong"; }
    
    strengthBar.className = "h-full transition-all duration-300 " + color;
    strengthBar.style.width = score + "%";
    strengthText.textContent = text;
    charCount.textContent = pw.length + " chars";
    submitBtn.disabled = score < 50;
});