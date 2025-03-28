// Initialize Combo Box
function initComboBox(fieldName) {
    const input = document.querySelector(`#${fieldName}`);
    const hiddenInput = document.querySelector(`#${fieldName}_id`);
    const comboBoxOptions = document.querySelector(`#${fieldName}-options`);
    const arrowButton = document.querySelector(`#${fieldName}-btn`);

    // Handle arrow button click
    if (arrowButton) {
        arrowButton.addEventListener("click", (e) => {
          e.stopPropagation(); // Prevent click from closing immediately
          if (comboBoxOptions.style.display === "block") {
            comboBoxOptions.style.display = "none"; // Hide if visible
          } else {
            comboBoxOptions.style.display = "block"; // Show dropdown
            input.focus(); // Also focus input for smooth UX
          }
        });
      }
  
    // Show/Hide Options When Typing or Clicking
    input.addEventListener("focus", () => {
      comboBoxOptions.style.display = "block";
    });

    // Handle blur event to check for new entries in the category
    if (fieldName === "category") {
        input.addEventListener("blur", (e) => {
        const typedCategory = e.target.value.trim();
        if (typedCategory !== "") {
            updateSubcategories(typedCategory);
        }
        });
    }
 
    // filter options based on input
    input.addEventListener("input", (e) => {
        const inputValue = e.target.value.toLowerCase();
        const allOptions = Array.from(comboBoxOptions.querySelectorAll("li"));
      
        let hasMatch = false;
        allOptions.forEach((option) => {
          const optionName = option.dataset.name.toLowerCase();
          if (optionName.includes(inputValue)) {
            option.style.display = "block";
            hasMatch = true;
          } else {
            option.style.display = "none";
          }
        });
      
        // Show/Hide Dropdown Based on Matches
        comboBoxOptions.style.display = hasMatch ? "block" : "none";
      
    });
  
    // Handle Click on Option
    comboBoxOptions.addEventListener("click", (e) => {
      if (e.target.tagName === "LI" || e.target.closest("li")) {
        const selectedOption = e.target.closest("li");
        input.value = selectedOption.dataset.name;
        hiddenInput.value = selectedOption.dataset.id;
  
        // Hide dropdown after selecting
        comboBoxOptions.style.display = "none";
      }
    });
  
    // Hide Options When Clicking Outside
    document.addEventListener("click", (e) => {
      if (
        !comboBoxOptions.contains(e.target) &&
        e.target !== input &&
        e.target !== arrowButton
      ) {
        comboBoxOptions.style.display = "none";
      }
    });
}

function updateActiveOption(fieldName, selectedId) {
    const comboBoxOptions = document.querySelector(`#${fieldName}-options`);
    const allOptions = Array.from(comboBoxOptions.querySelectorAll("li"));
  
    // Remove active styles from all options
    allOptions.forEach((option) => {
      option.classList.remove("bg-indigo-600", "text-white", "font-semibold");
      const checkIcon = option.querySelector(".check-icon");
      if (checkIcon) {
        checkIcon.classList.add("hidden");
      }
    });
  
    // Convert selectedId to string for proper comparison
    const selectedOption = allOptions.find(
      (option) => option.dataset.id === String(selectedId)
    );
  
    if (selectedOption) {
      selectedOption.classList.add("bg-indigo-600", "text-white", "font-semibold");
  
      // Show checkmark if available
      let checkIcon = selectedOption.querySelector(".check-icon");
      if (!checkIcon) {
        checkIcon = document.createElement("span");
        checkIcon.className =
          "check-icon absolute inset-y-0 left-0 flex items-center pl-1.5 text-white";
        checkIcon.innerHTML = `
          <svg class="size-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clip-rule="evenodd" />
          </svg>
        `;
        selectedOption.prepend(checkIcon);
      }
  
      // Ensure the checkmark is visible
      if (checkIcon) {
        checkIcon.classList.remove("hidden");
      }
    }
}

// Track the last selected category to compare changes
let previousCategory = "";

// Handle Category Change and Fetch Subcategories
function handleCategoryChange() {
  const categoryInput = document.querySelector("#category");
  const categoryId = document.querySelector("#category_id").value;
  const typedCategory = categoryInput.value.trim();

  // Always show subcategory to prevent disappearing
  const subCategoryContainer = document.querySelector("#sub-category-container");
  subCategoryContainer.style.display = "block";

  // Check if the category value has changed
  if (typedCategory !== previousCategory) {
    // Reset subcategory only if the category value is different
    if (typedCategory === "" || categoryId === "") {
      resetSubcategory(true); // Clear subcategory only if the category is cleared
    } else {
      resetSubcategory(false); // Keep the subcategory input when typing
    }
  }

  // If the input is cleared, reset the subcategory and stop
  if (typedCategory === "") {
    resetSubcategory(true); // Clear and hide subcategory if the category is fully cleared
    previousCategory = "";
    return;
  }

  // If a valid category is selected from the dropdown, update subcategories
  if (categoryId) {
    updateSubcategories(categoryInput.value);
    previousCategory = categoryInput.value; // Track selected category
  } else if (typedCategory !== "") {
    // For a new category, reset subcategory options but keep it visible
    updateSubcategories(typedCategory);
  }
}

// Reset Subcategory When Category Changes
function resetSubcategory() {
    const subCategoryInput = document.querySelector("#sub-category");
    const subCategoryHiddenInput = document.querySelector("#sub-category_id");
    const subCategoryOptions = document.querySelector("#sub-category-options");
  
    subCategoryInput.value = "";
    subCategoryHiddenInput.value = "";
    subCategoryOptions.innerHTML = ""; 
}

// Fallback if manually triggered
function selectOption(fieldName, id, name) {
    const input = document.querySelector(`#${fieldName}`);
    const hiddenInput = document.querySelector(`#${fieldName}_id`);
  
    input.value = name;
    hiddenInput.value = id;
  
    // Hide the dropdown after selecting
    document.querySelector(`#${fieldName}-options`).style.display = "none";
  
    // Update active option with the checkmark and styles
    updateActiveOption(fieldName, id);
  
    // Handle category-specific changes
    if (fieldName === "category") {
      handleCategoryChange(); // Update subcategories on category change
    }
  }

function updateSubcategories(categoryName) {
    const subCategoryContainer = document.querySelector("#sub-category-container");
    const subCategoryOptions = document.querySelector("#sub-category-options");
    const subCategoryInput = document.querySelector("#sub-category");
    const subCategoryHiddenInput = document.querySelector("#sub-category_id");
  
    // Clear previous options
    subCategoryOptions.innerHTML = "";
  
    if (!categoryName || categoryName.trim() === "") {
      subCategoryContainer.style.display = "none";
      return;
    }
  
    // Fetch subcategories from the server
    fetch(`/api/subcategories/${encodeURIComponent(categoryName)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch subcategories");
        }
        return response.json();
      })
      .then((data) => {
        if (data.length === 0) {
          // Show empty subcategory for manual entry
          subCategoryContainer.style.display = "block";
          subCategoryOptions.innerHTML = `
            <li
              class="relative cursor-default py-2 pr-4 pl-8 text-gray-900 select-none"
              data-id=""
              data-name=""
            >
              <span class="block truncate text-gray-400">Type to create a new subcategory...</span>
            </li>
          `;
  
          subCategoryInput.value = "";
          subCategoryHiddenInput.value = "";
          subCategoryOptions.style.display = "none";
        } else {
          // Add new options dynamically
          data.forEach((sub) => {
            const option = document.createElement("li");
            option.className =
              "hover:bg-indigo-600 hover:text-white relative cursor-default py-2 pr-4 pl-8 text-gray-900 select-none";
            option.dataset.id = sub.id;
            option.dataset.name = sub.name;
            option.role = "option";
            option.tabIndex = -1;
            option.innerHTML = `<span class="block truncate">${sub.name}</span>`;
            option.onclick = () =>
              selectOption("sub-category", sub.id, sub.name);
            subCategoryOptions.appendChild(option);
          });
  
          // Show the sub-category container
          subCategoryContainer.style.display = "block";
  
          // Reinitialize the subcategory combo box after updating options
          initComboBox("sub-category");
        }
      })
      .catch((error) => {
        console.error("Error fetching subcategories:", error);
        subCategoryContainer.style.display = "block";
        subCategoryOptions.innerHTML = `
          <li
            class="relative cursor-default py-2 pr-4 pl-8 text-gray-900 select-none"
            data-id=""
            data-name=""
          >
            <span class="block truncate text-gray-400">Type to create a new subcategory...</span>
          </li>
        `;
      });
  }
  
  // Call initComboBox for All Combo Boxes
document.addEventListener("DOMContentLoaded", () => {
    initComboBox("category");
    initComboBox("sub-category"); // If you add another combo box, initialize it here
    // initComboBox("company");      // Add more as needed
});
  
