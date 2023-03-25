document.addEventListener('DOMContentLoaded', function() {
  // Save user's email to the local browser storage
  sessionStorage.setItem('username', document.querySelector('h2').innerHTML);
  
  // Use buttons to toggle between views
  // Add event handler for each of the nav bar buttons
  document.querySelectorAll('nav > button').forEach(button => {
    button.onclick = () => {
      document.querySelectorAll('nav > button').forEach(btn => btn.className = "btn btn-sm btn-outline-primary");
      button.className = "btn btn-sm btn-primary";
      const id = button.getAttribute('id');
      document.title = id.charAt(0).toUpperCase()+id.slice(1).toLowerCase();
      window.history.pushState({section: id}, '', `#${id}`);
      console.table(location.href, history.state.section);
      // Load appropriate view
      if (id === 'compose') compose_email();
      else load_mailbox(id);
    }
  });

  window.onhashchange = () => document.getElementById(history.state.section).click();
  
  document.querySelector('#inbox').click();
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  // By default, send button is disabled
  document.querySelector('#send-email').disabled = true;
  
  // All input fields are required
  document.querySelector('#compose-recipients').required = true;
  document.querySelector('#compose-subject').required = true;
  document.querySelector('#compose-body').required = true;

  // Set attributes
  document.querySelector('#compose-recipients').dataset.valid = false;
  document.querySelector('#compose-subject').dataset.valid = false;
  document.querySelector('#compose-body').dataset.valid = false;
  
  // Email body textarea CSS modifications  
  document.querySelector('#compose-body').style.marginBottom = '20px';
  document.querySelector('#compose-body').style.resize = 'none';
  document.querySelector('#compose-body').style.overflow = 'hidden';
  document.querySelector('#compose-body').style.overflowY = 'scroll';

  // Instructions color = #495057
  document.getElementById("info-recipients").style.color = "#495057";
  document.querySelector("#info-recipients").style.fontSize = "15px";

  const fields = document.querySelectorAll('[data-uniform="compose"]');
  
  // Get the list of all recipients, and save the valid ones in an array
  // Recipients are comma-separated, .split(',')
  let validRecipients = [];
  let enableSend = [];

  // Arrow functions do not support `this` => https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fields.forEach((field, idx) => {
    field.className = "form-control border-secondary";
    enableSend.push(field.dataset.valid);
    
    // The input event fires when the value of an <input>, <select>, or <textarea> element has been changed. => https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event
    const isRecipients = field.getAttribute('id') === 'compose-recipients';
    field.oninput = () => {
      if (isRecipients) {
        validRecipients = []; 
        
        field.value.split(',').forEach(idx => { 
          // trim() remove whitespace
          idx = idx.trim();
          // RegEx representation of an email address => /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/g
          if (idx.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/g)) validRecipients.push(idx);
        }); 
      }
      
      const length = isRecipients ? validRecipients.length : field.value.match(/\S+/gm);
      if(!length) {  
        field.className = "form-control border-danger";
        field.dataset.valid = false;
      } else {
        field.className = "form-control border-success";
        field.dataset.valid = true;
      }
      enableSend[idx] = field.dataset.valid;
    
      // If all fields are valid, enable send email, i.e., submit button
      if (enableSend.every(inputField => inputField === 'true')) {
        document.querySelector('#send-email').disabled = false;
      // Else if already enabled and field is invalid, disable it
      } else {
        document.querySelector('#send-email').disabled = true;
      }
    };
    
    field.onchange = () => {
      if (isRecipients) console.table(validRecipients);
      console.table(enableSend);
    }
  });

  const form = document.querySelector('#compose-form');
  const feedback = document.createElement('span');
  feedback.style.marginLeft = '1rem'; 
  feedback.setAttribute("id", "feedback");


  // If the email is sent successfully, the route will respond with a 201 status code and a JSON response of {"message": "Email sent successfully."}.
  form.onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: validRecipients.join(','),
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      response = Object.keys(result)[0]; 
      result = Object.values(result)[0];
      
      console.log(result);
      feedback.innerHTML = result;
      
      // Success
      if (response === 'message') {
        feedback.style.color = 'green';
        feedback.insertAdjacentHTML('afterbegin', '<span class="material-symbols-outlined">done_all</span>');
        form.appendChild(feedback);
        setTimeout(() => {
          form.removeChild(feedback);
          load_mailbox('sent');
        }, 2000);
      } else {
        // Error
        document.querySelector('#compose-recipients').className = "form-control border-danger";
        feedback.style.color = 'red';
        feedback.insertAdjacentHTML('afterbegin', '<span class="material-symbols-outlined">cancel</span> ');
        document.querySelector('#send-email').disabled = true;
        form.appendChild(feedback);
        setTimeout(() => {
          form.removeChild(feedback);
        }, 5000);
      }
    });
    
    // Prevent submission
    return false;
  };

}

// GET /emails/<str:mailbox>
function load_mailbox(mailbox) {
  document.querySelector('#emails-view').innerHTML = '';

  document.querySelector(`#${mailbox}`).className = "btn btn-sm btn-primary"

  // Show the mailbox and hide other views
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      /* 
        {
        "id": 100,
        "sender": "foo@example.com",
        "recipients": ["bar@example.com"],
        "subject": "Hello!",
        "body": "Hello, world!",
        "timestamp": "Jan 2 2020, 12:00 AM",
        "read": false,
        "archived": false
        }
      */

      // When a mailbox is visited, the application should first query the API for the latest emails in that mailbox.
      // When a mailbox is visited, the name of the mailbox should appear at the top of the page (this part is done for you).
      // Each email should then be rendered in its own box (e.g. as a <div> with a border) that displays who the email is from, 
      // what the subject line is, and the timestamp of the email.
      // If the email is unread, it should appear with a white background. 
      // If the email has been read, it should appear with a gray background.
      emails.forEach(email => {
        if (mailbox === 'archive' && email['archived'] === 'false') {
          // Skip current iteration
          return;
        }
        
        const emailParentDiv = document.createElement('div');
        emailParentDiv.style.width = '100%';  
        emailParentDiv.style.maxHeight = '52px';
        emailParentDiv.style.border = '1px solid black';
        emailParentDiv.style.color = 'black';
        emailParentDiv.setAttribute('id', 'email');
        
        // unread = white & read = gray
        if (email["read"]) emailParentDiv.style.background = 'rgb(173, 173, 173)';
        else emailParentDiv.style.background = 'rgb(255, 255, 255)';

        // Each email should then be rendered in its own box (e.g. as a <div> with a border) that displays who the email is from, 
        // what the subject line is, and the timestamp of the email.

        const sender = document.createElement('div');
        sender.innerHTML = (mailbox === 'sent') ? `${email["recipients"]}` : email['sender'];
        sender.style.padding = '10px';
        sender.style.paddingRight = '15px';
        sender.style.justifyContent = 'flex-start';
        sender.style.gridArea = '1 / 1 / 6 / 2';
        emailParentDiv.appendChild(sender);
        
        const subject = document.createElement('div');
        subject.innerHTML = email['subject'];
        subject.style.gridArea = '1 / 2 / 6 / 5';
        subject.style.padding = '10px';
        subject.style.alignItems = 'flex-start';
        emailParentDiv.appendChild(subject);
        
        const timestamp = document.createElement('div');
        timestamp.innerHTML = email['timestamp'];
        timestamp.style.padding = '10px';
        timestamp.style.justifyContent = 'flex-end';
        timestamp.style.gridArea = '1 / 5 / 6 / 6';
        timestamp.style.color = '#495057';
        emailParentDiv.appendChild(timestamp);

        // Load the email on click
        emailParentDiv.addEventListener('click', function() {
          // Show the message and hide other views
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'none';
          document.querySelector('#message-view').style.display = 'block';
          
          // Mark received emails "read" on click
          if (mailbox !== 'sent') {
            fetch(`/emails/${email['id']}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
            })
            .then(response => {
              console.log(response);  
            });
          }
            

          document.querySelector('#message-view').innerHTML = '';
          // GET /emails/<int:email_id>
          fetch(`/emails/${email['id']}`)
          .then(response => response.json())
          .then(message => {
            // Print emails
            console.table(emails);
        
        
            const view = document.querySelector('#message-view');
            
            const header = document.createElement('div');

            // From: sender@example.com
            const from = document.createElement('p');
            from.innerHTML = 'From: ';
            from.style.fontWeight = 'bold';
            from.style.marginBottom = '5px';
            const sender = document.createElement('span');
            sender.innerHTML = message['sender'];
            sender.style.fontWeight = 'normal';
            from.appendChild(sender);
            header.appendChild(from);

            // To: recipients
            const to = document.createElement('p');
            to.innerHTML = 'To: ';
            to.style.fontWeight = 'bold';
            to.style.marginBottom = '5px';
            const recipient = document.createElement('span');
            recipient.innerHTML = message['recipients'];
            recipient.style.fontWeight = 'normal';
            to.appendChild(recipient);
            header.appendChild(to);

            // Subject: Title
            const subject = document.createElement('p');
            subject.innerHTML = 'Subject: ';
            subject.style.fontWeight = 'bold';
            subject.style.marginBottom = '5px';
            const title = document.createElement('span');
            title.innerHTML = message['subject'];
            title.style.fontWeight = 'normal';
            subject.appendChild(title);
            header.appendChild(subject);

            // Timestamp : Date / Time
            const timestamp = document.createElement('p');
            timestamp.innerHTML = 'Timestamp: ';
            timestamp.style.fontWeight = 'bold';
            timestamp.style.marginBottom = '5px';
            const time = document.createElement('span');
            time.innerHTML = message['timestamp'];
            time.style.fontWeight = 'normal';
            timestamp.appendChild(time);
            header.appendChild(timestamp);

            // Reply button
            const reply = document.createElement('button');
            reply.innerHTML = 'Reply';
            reply.setAttribute('id', 'reply');
            reply.className = "btn btn-sm btn-outline-primary";
            reply.onclick = () => reply.style.boxShadow = 'none';
            // Reply icon 
            reply.insertAdjacentHTML('beforeend',`<span class="material-symbols-outlined">reply</span>`);
            header.appendChild(reply);

            // On click, fetch and pre-fill compose form 
            reply.onclick = () => {
              // Display form
              compose_email();
            
              document.querySelectorAll('[data-uniform="compose"]').forEach(field => field.dataset.valid = true);
              let send = message['sender'];
              let receive = message['recipients'];

              
              if (mailbox !== 'sent') { 
                // swap values 
                if (receive.length > 1){
                  let user = document.querySelector('h2').innerHTML;
                  [receive[receive.indexOf(user)], send] = [send, user];
                  console.log(receive);
                } else {
                  [send, receive] = [receive, send];
                }
              } 
              // Convert date to human readable format
              let date = new Date(message['timestamp']);

              // If there are multiple recipients, 
              // Pre-fill form  
              document.querySelector('#compose-recipients').value = receive;
              // Trigger input event to validate the input field
              document.querySelector('#compose-recipients').dispatchEvent(new Event('input'));
              // If the subject has prefix do nothing, else add prefix to it
              document.querySelector('#compose-subject').value = message['subject'].startsWith('Re:') ? message['subject'] : `Re: ${message['subject']}`
              // Trigger input event to validate the input field
              document.querySelector('#compose-subject').dispatchEvent(new Event('input'));

              // User must trigger input event
              document.querySelector('#compose-body').value = '\r\n\r\n\r\n'+`On ${date.toLocaleString('en-US', {year: "numeric", month: "long", day: "numeric", hour: 'numeric', minute: 'numeric', hour12: true })} ${message['sender']} wrote:\r\n${message['body']}`;
            };
            
            /* 
              When viewing an Inbox email, the user should be presented with a button that lets them archive the email. 
              When viewing an Archive email, the user should be presented with a button that lets them unarchive the email. 
              This requirement does not apply to emails in the Sent mailbox.
            */


            // Archive button, not available on sent emails
            if (mailbox !== 'sent') {
              const archive = document.createElement('button');
              archive.innerHTML = message['archived'] ? 'Unarchive' : 'Archive';
              archive.setAttribute('id', 'archive');
              archive.className = "btn btn-sm btn-outline-primary";
              reply.style.margin = '10px';
              archive.style.margin = '10px';  
              if (archive.innerHTML === 'Archive') {
                // Archive button
                archive.insertAdjacentHTML('beforeend', '<span class="material-symbols-outlined">archive</span>');
              } else {
                // Unarchive button
                archive.insertAdjacentHTML('beforeend', '<span class="material-symbols-outlined">unarchive</span>');
              }
              // Archive or Unarchive email
              archive.onclick = () => {
                if (mailbox !== 'sent') {
                  archive.style.boxShadow = 'none';
                  // PUT /emails/<int:email_id>
                  fetch(`/emails/${email['id']}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: archive.innerHTML.startsWith('Archive') ? true : false
                    })
                  })
                  .then(response => {
                    console.log(response);  
                    // Once an email has been archived or unarchived, load the user’s inbox.
                    if (response.ok) load_mailbox('inbox');
                  });
                }
              };
              header.appendChild(archive);

              if (message['read']) {
                // "Mark as unread" button
                const unread = document.createElement('button');
                unread.innerHTML = 'Mark as unread';
                unread.setAttribute('id', 'unread');
                unread.style.margin = '10px';
                unread.className = "btn btn-sm btn-outline-primary";
                unread.insertAdjacentHTML('beforeend',`<span class="material-symbols-outlined">mark_as_unread</span>`);

                if (mailbox !== 'sent') {
                  unread.onclick = () => {
                    unread.style.boxShadow = 'none';
                    // PUT /emails/<int:email_id>
                    fetch(`/emails/${email['id']}`, {
                      method: 'PUT',
                      body: JSON.stringify({
                          read: false
                      })
                    })
                    .then(response => {
                      console.log(response);  
                      // Once an email has been archived or unarchived, load the user’s inbox.
                      if (response.ok) load_mailbox('inbox');
                    });
                  };
                }

                header.appendChild(unread);
              }
            }
            
            // Horizontal line
            const hr = document.createElement('hr');
            header.appendChild(hr);
            
            document.querySelector('#message-view').appendChild(header);
            
            const body = document.createElement('textarea');
            body.style.backgroundColor = 'transparent';
            body.style.border = 'none';   
            body.className = 'form-control';  
            body.setAttribute('id', 'display-body');
            body.disabled = true;
            body.style.color = 'black';
            body.value = message['body'];
            document.querySelector('#message-view').appendChild(body);
            body.style.height = body.scrollHeight + 'px';
          });

        });
        
        document.querySelector('#emails-view').appendChild(emailParentDiv);
      });
    });
}



