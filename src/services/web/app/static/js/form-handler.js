document.addEventListener("DOMContentLoaded", function () {
    // Elements
    const categoryDropdown = document.getElementById("category");
    const newCategoryContainer = document.getElementById("new-category-container");
    const subCategoryDropdown = document.getElementById("sub-category");
    const newSubCategoryContainer = document.getElementById("new-subcategory-container");
    const speakerInputs = document.querySelectorAll("#speaker-inputs input");

    /**
     * Handles category change event.
     * - Shows "New Category" input if "Other" is selected.
     * - Fetches subcategories from the backend and updates the dropdown.
     */
    function handleCategoryChange() {
        const selectedCategory = categoryDropdown.value;
        console.log("Selected Category:", selectedCategory);

        // Toggle new category input visibility
        newCategoryContainer.style.display = (selectedCategory === "Other") ? "block" : "none";

        // Clear previous subcategories
        subCategoryDropdown.innerHTML = "";

        // Fetch subcategories from Flask API
        if (selectedCategory !== "Other") {
            updateSubcategories(selectedCategory);
        }
    }

    /**
     * Updates subcategory dropdown based on selected category.
     */
    function updateSubcategories(selectedCategory) {
        function appendOption(value, textContent) {
            let option = document.createElement("option");
            option.value = value;
            option.textContent = textContent;
            subCategoryDropdown.appendChild(option);
        }

        fetch(`/subcategories/${selectedCategory}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    newSubCategoryContainer.style.display = "block";
                    selectedCategory.value = "Other"
                    console.log("No subcategories found for this category.");
                } else {
                    data.forEach(({ name }) => appendOption(name, name));
                    appendOption("Other", "Other");
                }

                // Check if the pre-selected subcategory is "Other"
                const selectedCategory = categoryDropdown.value;
                const selectedSubCategory = "{{ recording.subcategory|default('') }}";
                if (selectedSubCategory === "Other") {
                    newSubCategoryContainer.style.display = "block";
                }
            })
            .catch(error => console.error("Error fetching subcategories:", error));
    }

    /**
     * Handles subcategory change event.
     * - Shows "New Subcategory" input if "Other" is selected.
     */
    function handleSubCategoryChange() {
        if (categoryDropdown.value === "Other" && subCategoryDropdown.value === "") {
            newSubCategoryContainer.style.display = "block";
            let option = document.createElement("option");
            option.value = "Other";
            option.textContent = "Other";
            subCategoryDropdown.appendChild(option);
            return;
        }
        const selectedSubCategory = subCategoryDropdown.value;
        console.log("Selected Subcategory:", selectedSubCategory);
        newSubCategoryContainer.style.display = (selectedSubCategory === "Other") ? "block" : "none";
    }

    /**
     * Validates and processes speaker name assignments.
     */
    function validateSpeakerNames() {
        speakerInputs.forEach(input => {
            const speakerId = input.id;
            const speakerName = input.value.trim();
            console.log(`Assigning ${speakerId} to ${speakerName || "undefined"}`);
        });
    }

    // Attach event listeners
    categoryDropdown.addEventListener("change", handleCategoryChange);
    subCategoryDropdown.addEventListener("change", handleSubCategoryChange);
    speakerInputs.forEach(input => {
        input.addEventListener("input", validateSpeakerNames);
    });

    // Initial trigger in case of a default value
    handleCategoryChange();
    handleSubCategoryChange();
});