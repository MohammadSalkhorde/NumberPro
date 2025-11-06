// تنظیم پیش‌فرض: تم تاریک فعال و علامت خورشید نمایش داده شود
document.addEventListener("DOMContentLoaded", function () {
    const darkBtn = document.getElementById("darkModeBtn");
    const lightBtn = document.getElementById("lightModeBtn");
    const lightStyle = document.getElementById("lightStyle");
    const menuToggle = document.getElementById("menuToggle");
    const mobileMenu = document.getElementById("mobileMenu");

    // نمایش دکمه مناسب برای حالت تاریک
    darkBtn.style.display = "none";
    lightBtn.style.display = "inline-block";

    // سوییچ به حالت تاریک
    darkBtn.addEventListener("click", () => {
        lightStyle.disabled = true;
        darkBtn.style.display = "none";
        lightBtn.style.display = "inline-block";
    });

    // سوییچ به حالت روشن
    lightBtn.addEventListener("click", () => {
        lightStyle.disabled = false;
        lightBtn.style.display = "none";
        darkBtn.style.display = "inline-block";
    });

    // باز شدن منو با موس
    menuToggle.addEventListener("mouseenter", () => {
        menuToggle.classList.add("active");
        mobileMenu.classList.add("active");
    });

    // بسته شدن منو با خروج موس
    mobileMenu.addEventListener("mouseleave", () => {
        mobileMenu.classList.remove("active");
        menuToggle.classList.remove("active");
    });

    // باز/بستن منو در موبایل با کلیک
    menuToggle.addEventListener("click", () => {
        menuToggle.classList.toggle("active");
        mobileMenu.classList.toggle("active");
    });

    // بستن منو با کلیک بیرون از آن
    document.addEventListener("click", function (e) {
        if (!mobileMenu.contains(e.target) && !menuToggle.contains(e.target)) {
            mobileMenu.classList.remove("active");
            menuToggle.classList.remove("active");
        }
    });
});





const backToTopBtn = document.getElementById("backToTop");

window.addEventListener("scroll", () => {
  if (window.scrollY > 300) {  // وقتی صفحه 300 پیکسل پایین رفت دکمه نمایش داده شود
    backToTopBtn.style.display = "block";
  } else {
    backToTopBtn.style.display = "none";
  }
});

backToTopBtn.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});



const userMenuBtn = document.getElementById('userMenuBtn');
const userMenu = document.querySelector('.user-menu');

// دسکتاپ - باز و بسته شدن منو با موس
userMenu.addEventListener('mouseenter', () => {
  userMenu.classList.add('open');
  userMenuBtn.setAttribute('aria-expanded', 'true');
});
userMenu.addEventListener('mouseleave', () => {
  userMenu.classList.remove('open');
  userMenuBtn.setAttribute('aria-expanded', 'false');
});

// موبایل - باز و بسته شدن با کلیک
userMenuBtn.addEventListener('click', (e) => {
  e.preventDefault();
  userMenu.classList.toggle('open');
  const expanded = userMenuBtn.getAttribute('aria-expanded') === 'true';
  userMenuBtn.setAttribute('aria-expanded', String(!expanded));
});



  document.addEventListener('DOMContentLoaded', function () {
    const userBtn = document.getElementById('userMenuBtn');
    const dropdown = document.getElementById('userDropdown');

    let isOpen = false;

    userBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      isOpen = !isOpen;
      dropdown.style.opacity = isOpen ? '1' : '0';
      dropdown.style.visibility = isOpen ? 'visible' : 'hidden';
      dropdown.style.transform = isOpen ? 'translateY(0)' : 'translateY(-10px)';
    });

    // بسته شدن منو با کلیک بیرون
    document.addEventListener('click', function () {
      isOpen = false;
      dropdown.style.opacity = '0';
      dropdown.style.visibility = 'hidden';
      dropdown.style.transform = 'translateY(-10px)';
    });
  });


  document.addEventListener("DOMContentLoaded", function () {
    const darkBtn = document.getElementById("darkModeBtn");
    const lightBtn = document.getElementById("lightModeBtn");
    const lightStyle = document.getElementById("lightStyle");
    const logo = document.getElementById("siteLogo");

    function applyTheme(theme) {
      const isLight = theme === "light";
  
      lightStyle.disabled = !isLight;
      darkBtn.style.display = isLight ? "inline-block" : "none";
      lightBtn.style.display = isLight ? "none" : "inline-block";
  
      if (logo) {
          const newSrc = isLight ? logo.dataset.light : logo.dataset.dark;
          if (newSrc) logo.src = newSrc;
      }
  
      document.body.classList.toggle("dark-mode", !isLight);  // این خط جدید
  
      localStorage.setItem("theme", theme);
  }

  

    // رویداد کلیک برای تغییر تم
    darkBtn.addEventListener("click", () => applyTheme("dark"));
    lightBtn.addEventListener("click", () => applyTheme("light"));

    // استفاده از تم ذخیره‌شده یا پیش‌فرض (dark)
    const savedTheme = localStorage.getItem("theme") || "dark";
    applyTheme(savedTheme);
});



  const toggleBtn = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  const icon = toggleBtn.querySelector('i');

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    nav.classList.toggle('open');
    icon.classList.toggle('rotate');
  });

  document.addEventListener('click', (e) => {
    const isClickInside = nav.contains(e.target) || toggleBtn.contains(e.target);
    if (!isClickInside && nav.classList.contains('open')) {
      nav.classList.remove('open');
      icon.classList.remove('rotate');
    }
  });