document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => loadMailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => loadMailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => loadMailbox('archive'));
  document.querySelector('#compose').addEventListener('click', composeEmail);
  document.querySelector('#send-email').addEventListener('click', sendData);

  // By default, load the inbox
  loadMailbox('inbox');
});

function composeEmail() {

  // Switch to compose view
  showElements(document.querySelector('#compose-view'))
  hideElements(document.querySelector('#email-view'), document.querySelector('#emails-view'))


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

async function loadMailbox(mailbox) {
  
  // Switch to mailbox view
  showElements(document.querySelector('#emails-view'))
  hideElements(
    document.querySelector('#compose-view'), 
    document.querySelector('#email-view'),
    document.querySelector('#message')
  )

  // Show the mailbox name
  const mailboxName = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);
  document.querySelector('#mailbox-header').innerText = mailboxName;

  // Load and display mailbox data
  const mailboxElements = await loadData(mailboxName.toLowerCase())
  if (mailbox == 'sent'){
    showElements(document.querySelector('#archive'))
  }
  else{
    showElements(document.querySelector('#archive'))
  }
  if (mailboxElements.length == 0){
    // Display a blank message if mailbox is empty
    displayBlankMsg('info', mailbox);
  }
  // Display mailbox elements
  displayMailbox(mailboxElements);
}

async function viewEmail(emailId){
  // Switch to email view
  showElements(document.querySelector('#email-view'));
  hideElements(document.querySelector('#emails-view'));
  // Reset email header
  document.querySelector('#header-sender p').innerText = '';
  document.querySelector('#header-recipients p').innerText = '';
  document.querySelector('#header-subject p').innerText = '';
  document.querySelector('#header-timestamp p').innerText = '';

  const emailData = await loadData(emailId);   // load Email data
  await markRead(emailId, emailData.archived) // mark email as read
  // Fill header with the new data
  document.querySelector('#header-sender p').innerText = emailData.sender;
  document.querySelector('#header-recipients p').innerText = emailData.recipients;
  document.querySelector('#header-subject p').innerText = emailData.subject;
  document.querySelector('#header-timestamp p').innerText = emailData.timestamp;
  // display Emails content
  document.querySelector('#email-view > p').innerText = emailData.body;
  // Reset event listeners for reply and archive buttons
  resetEventListeners(document.querySelector('#reply'), document.querySelector('#archive'));
  const replyButton = document.querySelector('#reply')
  const archiveButton = document.querySelector('#archive')
  archiveButton.innerHTML = (emailData.archived == false) ? 'archive' : 'Unarchive'

  // Adding eventlisteners to reply and archive buttons
  replyButton.addEventListener('click', () => {
    replyEmail(emailData);
  });

  archiveButton.addEventListener('click', () => {
    archiveEmail(emailId, emailData.archived ? false : true);
  });

}


function sendData() {
  // Getting user inputs
  const recipients = document.querySelector('#compose-recipients').value.trim();
  const subject = document.querySelector('#compose-subject').value.trim();
  const body = document.querySelector('#compose-body').value.trim();

  // Ensuring that user inputs are valid
  if (!recipients || !subject || !body) {
    // Handle the case where any value is empty or zero
    alert('Please fill out all fields before sending.');
    return; // Exit the function
  }

  // Sending data
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json());
}


async function loadData(mailBox) {
  // Loading emails
  try {
    const emails = await fetch(`/emails/${mailBox}`);
    return emails.json();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}


async function archiveEmail(emailId, bool) {
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: bool
    })
  })
  .then(response => {
      loadMailbox('inbox');  // load inbox after archiving
  });
}


async function markRead(emailId, bool){
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true,
        archived: bool
    })
  })
}

function displayMailbox(mailboxEmails) {
  // Clear existing mailbox list
  const mailboxList = document.querySelector('#mailbox');
  mailboxList.innerHTML = '';

  // Convert mailboxEmails object to an array of email elements
  const mailboxElements = Object.values(mailboxEmails);

  // Iterate through each email element to create the display
  mailboxElements.forEach(element => {
    // Create a list item for the email
    const elementLi = document.createElement("li");
    elementLi.setAttribute("class", "list-group-item list-group-item-action");

    // Add 'not-read' class if the email has not been read
    if (element.read === false) {
      elementLi.classList.add('not-read'); // Highlight unread emails
    }

    // Add click event to view/open the email when clicked
    elementLi.addEventListener('click', () => viewEmail(element.id));

    // Create a container for the email header
    const elementDiv = document.createElement("div");
    elementDiv.setAttribute("class", "d-flex w-100 justify-content-between");

    // Create a small element for the sender's name
    const elementSmallSender = document.createElement("small");
    elementSmallSender.innerText = `from: ${element.sender}`;
    elementSmallSender.setAttribute("class", "header-sender");

    // Create a small element for the email timestamp
    const elementSmallTime = document.createElement("small");
    elementSmallTime.innerText = element.timestamp;

    // Create a paragraph for the email subject and body
    const elementP = document.createElement("p");
    elementP.setAttribute("class", "mb-1");
    elementP.innerHTML = `<b>${element.subject}</b>&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;${element.body}`;

    // Append the components to the list item
    elementLi.appendChild(elementDiv);
    elementDiv.appendChild(elementSmallSender);
    elementDiv.appendChild(elementSmallTime);
    elementLi.appendChild(elementP);

    // Append the list item to the mailbox list
    mailboxList.appendChild(elementLi);
  });
}


function replyEmail(email){
  composeEmail(); // Start composing a new email

  // Set the recipients field with the sender and list of recipients
  document.querySelector('#compose-recipients').value = email.sender + ', ' + email.recipients.join(", ");

  // Set the subject; prepend "Re: " if it isn't already present
  document.querySelector('#compose-subject').value = (!email.subject.startsWith('Re: ')) ? 'Re: ' + email.subject : email.subject;

  // Pre-fill the body of the email with the original message detai
  document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} wrote ${email.sender} wrote:\n\n${email.body}`;
}

function resetEventListeners(...elements){
  // Replace the exisiting elements with new elements
  elements.forEach((oldElement) => {
    // Clone old element and replace it
    newElement = oldElement.cloneNode(true)
    oldElement.replaceWith(newElement);
});
}

function displayBlankMsg(type, mailbox){
  // Define blank messages to display if mailbox is empty
  const messages = {
    'inbox': "You don't have any recieved emails yet!",
    'sent': "You did't send any emails yet!",
    'archive': "You didn't archive any emails yet"
  }
  const messageElement = document.querySelector("#message");
  showElements(messageElement)
  blankMessage = messages[mailbox];
  messageElement.classList.add(type);
  messageElement.innerText = blankMessage;
}


function showElements(...elements){
  // Show all given elements
  elements.forEach((element) => {
    element.classList.replace('hide', 'show');
});
}


function hideElements(...elements){
  // Hide all given elements
  elements.forEach((element) => {
    element.classList.replace('show', 'hide');
});
}