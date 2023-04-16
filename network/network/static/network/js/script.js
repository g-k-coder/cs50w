document.addEventListener("DOMContentLoaded", function () {
  //* All Posts and Following Posts
  if (location.pathname === "/" && document.querySelector("#createpost")) {
    const newPostBtn = document.querySelector("#newpost-btn");
    const newPostIcon = document.querySelector("#newpost-icon");
    const newPostForm = document.querySelector("#newpost-form");

    newPostBtn.onclick = function () {
      newPostForm.style.animationIterationCount = 1;

      this.setAttribute("disabled", "");
      if (newPostIcon.innerHTML === "expand_more") {
        newPostIcon.innerHTML = "expand_less";
        newPostForm.style.animation = "dropdown .5s forwards ease-in";
      } else {
        newPostIcon.innerHTML = "expand_more";
        newPostForm.style.animation = "popup .5s forwards ease-out";
      }
      setTimeout(() => {
        this.removeAttribute("disabled");
      }, 500);
    };
  } //* User profile

  if (document.querySelector("#follow")) {
    let followBtn = document.querySelector("#follow");

    followBtn.onclick = function () {
      (async () => {
        const response = await fetch(
          `/updateFollow/follow/${followBtn.dataset.user}/${followBtn.dataset.follower}`,
          {
            method: followBtn.innerHTML === "Follow" ? "POST" : "DELETE",
            headers: { "X-CSRFToken": getToken() },
          }
        );
        const result = await response.json();
        console.table(result);
        followBtn.innerHTML =
          followBtn.innerHTML === "Follow" ? "Unfollow" : "Follow";
        document.querySelector("#numFers").innerHTML = result["followers"];
      })();
    };
  }

  // Get the first occurrence of a like button and check if the user is even logged in
  try {
    if (!document.querySelector(".postLike").disabled) {
      let likeBtn = document.querySelectorAll(".postLike");
      likeBtn.forEach((like) => {
        like.onclick = () => {
          (async () => {
            const response = await fetch(
              `/updateFollow/like/${like.dataset.user}/${like.dataset.post}`,
              {
                method:
                  like.children[0].dataset.liked === "false"
                    ? "POST"
                    : "DELETE",
                headers: { "X-CSRFToken": getToken() },
              }
            );
            const result = await response.json();
            console.table(result);
            // Change data-liked from 0 to 1 or from 1 to 0
            const likeState = like.children[0].dataset.liked;
            like.children[0].dataset.liked =
              likeState === "true" ? "false" : "true";
            like.children[1].innerHTML = result["likes"];
          })();
        };
      });
    }
  } catch {}

  document.querySelectorAll('span[type="button"].postEdit').forEach((btn) => {
    btn.onclick = () => {
      // Get parent element to replace paragraph with textarea
      let post = document.querySelector(`.post[data-id='${btn.dataset.id}']`);

      let postContent = document.querySelector(
        `#id${btn.dataset.id}.postContent`
      );

      if (btn.dataset.state === "Edit") {
        let textarea = document.createElement("textarea");
        textarea.className = "postContent";
        textarea.setAttribute("id", `id${btn.dataset.id}`);
        textarea.setAttribute("autofocus", "");

        (async () => {
          const response = await fetch(`/edit/edit/${btn.dataset.id}`, {
            method: "POST",
            headers: { "X-CSRFToken": getToken() },
          });
          console.table(response);
          const result = await response.json();
          console.table(result);
          console.log("Status code: " + response.status);
          btn.innerHTML =
            '<span class="material-symbols-outlined">save</span>    Save';
          textarea.value = result["content"].replace(/"/g, "");

          post.replaceChild(textarea, postContent);
          resize(textarea);
          textarea.oninput = () => resize(textarea);
          btn.dataset.state = "Save";
        })();
      } else if (btn.dataset.state === "Save") {
        let div = document.createElement("div");
        div.className = "postContent";
        div.setAttribute("id", `id${btn.dataset.id}`);

        (async () => {
          const response = await fetch(`/edit/save/${btn.dataset.id}`, {
            method: "POST",
            headers: { "X-CSRFToken": getToken() },
            body: JSON.stringify(postContent.value.replace(/\n/g, "<br>")),
          });
          if (!response.ok) return alert(response.status);
          const result = await response.json();
          console.table(result);
          console.log("Status code: " + response.status);
          btn.innerHTML =
            '<span class="material-symbols-outlined">edit_note</span>    Edit';
          div.innerHTML = result.content;

          post.replaceChild(div, postContent);
          btn.dataset.state = "Edit";
        })();
      }
    };
  });

  // Check for paginator
  if (document.querySelector(".pagination")) {
    let toggleBtns = document.querySelectorAll(".pagination li");
    toggleBtns.forEach((btn) => {
      if (window.location.pathname !== localStorage.currentLocation)
        toggleBtns.forEach((toggleBtn) => (toggleBtn.className = "page-item"));

      btn.onclick = () => {
        toggleBtns.forEach((toggleBtn) => (toggleBtn.className = "page-item"));
        btn.className = "page-item active";

        localStorage.setItem(
          "pageButton",
          btn.children[0].getAttribute("href")
        );
        localStorage.setItem("currentPath", window.location.pathname);
      };
      
      if (!window.location.search.length) {
        // If there is paginator available and there is no search query, meaning it is the first page, set the pagination button 1 to active indicating it is the first page
        document.querySelector(
          `.page-item:has(a[href='?page=1']):not(li[name^='icon'])`
        ).className = "page-item active";
      } else if (
        localStorage.pageButton &&
        localStorage.currentPath === window.location.pathname
      ) {
        document.querySelector(
          `.page-item:has(a[href='${localStorage.pageButton}']):not(li[name^='icon'])`
        ).className = "page-item active";
      } 
    });

  }
});

// Get CSRF Token from cookies
function getToken() {
  const cookie = `; ${document.cookie}`.split(`; csrftoken=`);
  if (cookie.length === 2) return cookie.pop().split(";").shift();
}

// Dynamically resize textarea on input
function resize(textarea) {
  textarea.style.height = textarea.scrollHeight + "px";
}
