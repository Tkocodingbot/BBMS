
      // Multi-Select Dropdown Functionality
      const selectDisplay = document.getElementById("selectDisplay");
      const dropdownList = document.getElementById("dropdownList");
      const checkboxes = dropdownList.querySelectorAll(
        'input[type="checkbox"]'
      );
      const meetingForm = document.getElementById("meetingForm");

      selectDisplay.addEventListener("click", function (e) {
        e.stopPropagation();
        dropdownList.classList.toggle("open");
        selectDisplay.classList.toggle("open");
      });

      document.addEventListener("click", function (e) {
        if (!document.getElementById("attendeesSelect").contains(e.target)) {
          dropdownList.classList.remove("open");
          selectDisplay.classList.remove("open");
        }
      });

      dropdownList.addEventListener("click", function (e) {
        e.stopPropagation();
      });

      checkboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", updateDisplay);
      });

      function updateDisplay() {
        const selected = Array.from(checkboxes)
          .filter((cb) => cb.checked)
          .map((cb) => cb.value);

        if (selected.length === 0) {
          selectDisplay.innerHTML =
            '<span class="placeholder">Select attendees...</span>';
        } else {
          const tags = selected
            .map(
              (name) =>
                `<span class="tag">${name} <span class="remove" data-value="${name}">×</span></span>`
            )
            .join("");
          selectDisplay.innerHTML = `<div class="selected-tags">${tags}</div>`;

          selectDisplay.querySelectorAll(".remove").forEach((btn) => {
            btn.addEventListener("click", function (e) {
              e.stopPropagation();
              const value = this.getAttribute("data-value");
              const checkbox = Array.from(checkboxes).find(
                (cb) => cb.value === value
              );
              if (checkbox) {
                checkbox.checked = false;
                updateDisplay();
              }
            });
          });
        }
      }

      meetingForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const subject = document.getElementById("subject").value;
        const agenda = document.getElementById("agenda").value;
        const time = document.getElementById("time").value;
        const date = document.getElementById("date").value;
        const selectedAttendees = Array.from(checkboxes)
          .filter((cb) => cb.checked)
          .map((cb) => cb.value);
        const apologies = document.getElementById("apologies").value;
        const selectedTimeSlot = document.querySelector(".time-slot.selected");

        console.log({
          subject: subject,
          agenda: agenda,
          time: time,
          date: date,
          selectedSlot: selectedTimeSlot
            ? selectedTimeSlot.textContent
            : "None",
          slotDate: currentDate.toDateString(),
          attendees: selectedAttendees,
          apologies: apologies,
        });

        alert(
          "Meeting form submitted successfully!\n\nSubject: " +
            subject +
            "\nDate: " +
            currentDate.toDateString() +
            "\nTime Slot: " +
            (selectedTimeSlot ? selectedTimeSlot.textContent : "None") +
            "\nAttendees: " +
            (selectedAttendees.length > 0
              ? selectedAttendees.join(", ")
              : "None")
        );
      });

      // Time Slot Picker Functionality
      let currentDate = new Date(2021, 4, 29); // May 29, 2021
      const dateDisplay = document.getElementById("dateDisplay");
      const timeSlotsGrid = document.getElementById("timeSlotsGrid");
      const prevDateBtn = document.getElementById("prevDate");
      const nextDateBtn = document.getElementById("nextDate");

      // Generate time slots from 08:00 to 16:00
      function generateTimeSlots() {
        timeSlotsGrid.innerHTML = "";

        for (let hour = 8; hour <= 16; hour++) {
          const timeSlot = document.createElement("div");
          timeSlot.className = "time-slot";

          const hourStr = hour.toString().padStart(2, "0");
          timeSlot.textContent = `${hourStr}:00`;

          timeSlot.addEventListener("click", function () {
            // Remove selected class from all slots
            document.querySelectorAll(".time-slot").forEach((slot) => {
              slot.classList.remove("selected");
            });
            // Add selected class to clicked slot
            this.classList.add("selected");

            // Update the time input field
            document.getElementById("time").value = this.textContent;
          });

          timeSlotsGrid.appendChild(timeSlot);
        }
      }

      function updateDateDisplay() {
        const options = {
          weekday: "short",
          year: "numeric",
          month: "short",
          day: "numeric",
        };
        dateDisplay.textContent = currentDate.toLocaleDateString(
          "en-US",
          options
        );

        // Update date input field
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, "0");
        const day = String(currentDate.getDate()).padStart(2, "0");
        document.getElementById("date").value = `${year}-${month}-${day}`;
      }

      prevDateBtn.addEventListener("click", function () {
        currentDate.setDate(currentDate.getDate() - 1);
        updateDateDisplay();
      });

      nextDateBtn.addEventListener("click", function () {
        currentDate.setDate(currentDate.getDate() + 1);
        updateDateDisplay();
      });

      // External attendees array to store emails
let externalAttendees = [];

// Get elements
const addExternalBtn = document.getElementById('addExternalBtn');
const modal = document.getElementById('externalEmailModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelBtn = document.getElementById('cancelBtn');
const addEmailBtn = document.getElementById('addEmailBtn');
const externalEmailInput = document.getElementById('externalEmail');
const emailError = document.getElementById('emailError');
const externalAttendeesList = document.getElementById('externalAttendeesList');

// Open modal
addExternalBtn.addEventListener('click', function() {
  modal.style.display = 'flex';
  externalEmailInput.value = '';
  emailError.style.display = 'none';
  externalEmailInput.focus();
});

// Close modal
function closeModal() {
  modal.style.display = 'none';
  externalEmailInput.value = '';
  emailError.style.display = 'none';
}

closeModalBtn.addEventListener('click', closeModal);
cancelBtn.addEventListener('click', closeModal);

// Close modal when clicking outside
modal.addEventListener('click', function(e) {
  if (e.target === modal) {
    closeModal();
  }
});

// Validate email
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// Add email
function addExternalEmail() {
  const email = externalEmailInput.value.trim().toLowerCase();
  
  if (!email) {
    emailError.textContent = 'Please enter an email address';
    emailError.style.display = 'block';
    return;
  }
  
  if (!validateEmail(email)) {
    emailError.textContent = 'Please enter a valid email address';
    emailError.style.display = 'block';
    return;
  }
  
  if (externalAttendees.includes(email)) {
    emailError.textContent = 'This email is already in the list';
    emailError.style.display = 'block';
    return;
  }
  
  externalAttendees.push(email);
  renderExternalAttendees();
  closeModal();
}

addEmailBtn.addEventListener('click', addExternalEmail);

// Add email on Enter key
externalEmailInput.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    addExternalEmail();
  }
});

// Remove email
function removeExternalEmail(email) {
  externalAttendees = externalAttendees.filter(e => e !== email);
  renderExternalAttendees();
}

// Render external attendees list
function renderExternalAttendees() {
  if (externalAttendees.length === 0) {
    externalAttendeesList.innerHTML = '<span style="color: #999; font-size: 13px;">No external attendees added</span>';
    return;
  }
  
  externalAttendeesList.innerHTML = externalAttendees.map(email => `
    <div class="external-email-tag">
      <span>${email}</span>
      <button type="button" onclick="removeExternalEmail('${email}')">×</button>
    </div>
  `).join('');
}

      // Initialize
      generateTimeSlots();
      updateDateDisplay();
      renderExternalAttendees();