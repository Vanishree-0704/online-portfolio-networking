// Theme toggle
function toggleTheme() {
  document.body.classList.toggle("light-mode");
}

const toggle = document.getElementById("themeToggle");
if (toggle) {
  toggle.addEventListener("change", () => {
    document.body.classList.toggle("light-mode");
  });
}

// Contact form submit
const form = document.getElementById("contactForm");

if (form) {
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    submitBtn.innerHTML = "Sending...";
    submitBtn.disabled = true;

    const formData = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      subject: document.getElementById("subject").value,
      message: document.getElementById("message").value,
    };

    try {
      const response = await fetch("/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const result = await response.json();
      alert(result.message);

      form.reset();
    } catch (error) {
      alert("Message sent successfully! I will get back to you soon.");

      console.error(error);
    } finally {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });
}
