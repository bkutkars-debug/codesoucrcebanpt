const nodemailer = require("nodemailer");
const https = require("https");
const fs = require("fs");
const path = require("path");
require("dotenv").config();

const ADMIN_PRIMARY_EMAIL = process.env.ADMIN_EMAIL || "bkutkars@gmail.com";
const ADMIN_SECONDARY_EMAIL = process.env.ADMIN_SECONDARY_EMAIL || "bkutakrs@gmail.com";

const DATA_DIR = path.join(__dirname, "data");
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}
const NOTIFICATIONS_FILE = path.join(DATA_DIR, "signup_notifications.json");

/**
 * Dispatches an automated email to a recipient via FormSubmit's REST API.
 * FormSubmit delivers directly to real inboxes (@gmail.com).
 */
async function dispatchViaFormSubmit(recipientEmail, payload) {
  return new Promise((resolve) => {
    const postData = JSON.stringify(payload);
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referer": "http://localhost:5000",
        "Origin": "http://localhost:5000",
        "User-Agent": "CodeRescueAI/1.0"
      },
      timeout: 10000
    };

    const req = https.request(`https://formsubmit.co/ajax/${recipientEmail}`, options, (res) => {
      let data = "";
      res.on("data", (chunk) => { data += chunk; });
      res.on("end", () => {
        try {
          const parsed = JSON.parse(data);
          const isActivated = parsed.success === "true" || parsed.success === true;
          const needsActivation = (parsed.message || "").toLowerCase().includes("activation");
          resolve({
            statusCode: res.statusCode,
            success: res.statusCode === 200,
            delivered: isActivated,
            needsActivation: needsActivation,
            message: parsed.message || "Dispatched via FormSubmit",
            data: parsed
          });
        } catch (e) {
          resolve({
            statusCode: res.statusCode,
            success: res.statusCode === 200,
            delivered: res.statusCode === 200,
            message: data || "Dispatched via FormSubmit"
          });
        }
      });
    });

    req.on("error", (err) => {
      resolve({
        success: false,
        delivered: false,
        error: err.message
      });
    });

    req.on("timeout", () => {
      req.destroy();
      resolve({
        success: false,
        delivered: false,
        error: "FormSubmit request timed out after 10s"
      });
    });

    req.write(postData);
    req.end();
  });
}

/**
 * Sends a real sign-up notification message to bkutkars@gmail.com.
 * Uses official Gmail SMTP when credentials are in .env,
 * otherwise routes directly via FormSubmit to deliver to real Gmail inboxes.
 */
async function sendSignupNotification({ user, avatarSvg }) {
  const timestamp = new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata" });
  const subject = `🎉 New CodeRescue AI Signup: ${user.name} (${user.email})`;

  const textContent = `
New User Sign-Up on CodeRescue AI!
----------------------------------
User Name:  ${user.name}
User Email: ${user.email}
User ID:    ${user.id}
Signed At:  ${timestamp}
Avatar:     ${user.avatarSeed}

This real notification was automatically dispatched to ${ADMIN_PRIMARY_EMAIL}.
`.trim();

  // Generate direct Gmail Web compose link for instant manual trigger
  const gmailWebComposeUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(ADMIN_PRIMARY_EMAIL)}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(textContent)}`;

  // CHANNEL 1: Direct Gmail SMTP via Nodemailer
  if (process.env.GMAIL_USER && process.env.GMAIL_PASS) {
    try {
      const transporter = nodemailer.createTransport({
        service: "gmail",
        auth: {
          user: process.env.GMAIL_USER,
          pass: process.env.GMAIL_PASS
        }
      });

      const htmlContent = `
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0b1120; color: #f1f5f9; border-radius: 12px; overflow: hidden; border: 1px solid #1e293b;">
  <div style="background: linear-gradient(135deg, #0284c7, #6366f1); padding: 24px; text-align: center;">
    <h1 style="margin: 0; font-size: 24px; color: #ffffff;">CodeRescue AI</h1>
    <p style="margin: 6px 0 0; color: #e0e7ff; font-size: 14px;">New User Registration Notification</p>
  </div>
  <div style="padding: 24px;">
    <p style="font-size: 16px; margin: 0 0 16px;"><strong>${user.name}</strong> has just created an account on CodeRescue AI.</p>
    <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1; margin-bottom: 20px;">
      <tr style="border-bottom: 1px solid #1e293b;"><td style="padding: 8px 0; font-weight: bold; color: #94a3b8;">User Name:</td><td style="padding: 8px 0; color: #f1f5f9;">${user.name}</td></tr>
      <tr style="border-bottom: 1px solid #1e293b;"><td style="padding: 8px 0; font-weight: bold; color: #94a3b8;">User Email:</td><td style="padding: 8px 0; color: #38bdf8;">${user.email}</td></tr>
      <tr style="border-bottom: 1px solid #1e293b;"><td style="padding: 8px 0; font-weight: bold; color: #94a3b8;">User ID:</td><td style="padding: 8px 0; font-family: monospace; color: #f1f5f9;">${user.id}</td></tr>
      <tr style="border-bottom: 1px solid #1e293b;"><td style="padding: 8px 0; font-weight: bold; color: #94a3b8;">Signup Timestamp:</td><td style="padding: 8px 0; color: #f1f5f9;">${timestamp}</td></tr>
      <tr><td style="padding: 8px 0; font-weight: bold; color: #94a3b8;">Avatar Seed:</td><td style="padding: 8px 0; font-family: monospace; color: #a78bfa;">${user.avatarSeed}</td></tr>
    </table>
    <div style="background: #090e1a; padding: 12px 16px; border-radius: 6px; font-size: 12px; color: #94a3b8;">
      Delivered directly via Gmail SMTP to <strong>${ADMIN_PRIMARY_EMAIL}</strong>
    </div>
  </div>
</div>`.trim();

      const info = await transporter.sendMail({
        from: `"CodeRescue AI" <${process.env.GMAIL_USER}>`,
        to: `${ADMIN_PRIMARY_EMAIL}, ${ADMIN_SECONDARY_EMAIL}`,
        subject,
        text: textContent,
        html: htmlContent
      });

      console.log(`[REAL GMAIL SMTP DISPATCH] Delivered to ${ADMIN_PRIMARY_EMAIL}`);
      const logEntry = {
        timestamp,
        user,
        deliveryChannel: "gmail_smtp",
        recipient: ADMIN_PRIMARY_EMAIL,
        messageId: info.messageId,
        status: "delivered",
        gmailWebComposeUrl
      };
      saveNotificationLog(logEntry);

      return {
        success: true,
        deliveryChannel: "gmail_smtp",
        status: "delivered",
        recipient: ADMIN_PRIMARY_EMAIL,
        messageId: info.messageId,
        gmailWebComposeUrl
      };
    } catch (smtpErr) {
      console.warn("[GMAIL SMTP WARNING] Failed to send via Gmail SMTP, falling back to FormSubmit:", smtpErr.message);
    }
  }

  // CHANNEL 2: Cloud Delivery via FormSubmit API to bkutkars@gmail.com
  const formSubmitPayload = {
    _subject: subject,
    _template: "table",
    _captcha: "false",
    _replyto: user.email,
    "New User Name": user.name,
    "New User Email": user.email,
    "User ID": user.id,
    "Avatar Seed": user.avatarSeed,
    "Signup Timestamp": timestamp,
    "Detector Name": "coderescue-ai",
    "Admin Alert Target": ADMIN_PRIMARY_EMAIL
  };

  console.log(`[DISPATCHING EMAIL] Sending real signup alert to ${ADMIN_PRIMARY_EMAIL} and ${ADMIN_SECONDARY_EMAIL}...`);
  const [primaryRes, secondaryRes] = await Promise.all([
    dispatchViaFormSubmit(ADMIN_PRIMARY_EMAIL, formSubmitPayload),
    dispatchViaFormSubmit(ADMIN_SECONDARY_EMAIL, formSubmitPayload)
  ]);

  const needsActivation = primaryRes.needsActivation || secondaryRes.needsActivation;
  const isDelivered = primaryRes.delivered || secondaryRes.delivered;

  const resultStatus = isDelivered ? "delivered" : needsActivation ? "awaiting_activation" : "dispatched";

  const logEntry = {
    timestamp,
    user,
    deliveryChannel: "formsubmit_http",
    recipients: `${ADMIN_PRIMARY_EMAIL}, ${ADMIN_SECONDARY_EMAIL}`,
    status: resultStatus,
    needsActivation,
    primaryResponse: primaryRes,
    secondaryResponse: secondaryRes,
    gmailWebComposeUrl
  };
  saveNotificationLog(logEntry);

  console.log(`===============================================`);
  console.log(`[REAL EMAIL DISPATCH RESULT]`);
  console.log(`Recipient    : ${ADMIN_PRIMARY_EMAIL}`);
  console.log(`Channel      : FormSubmit HTTP API`);
  console.log(`Status       : ${resultStatus}`);
  if (needsActivation) {
    console.log(`ACTION NEEDED: FormSubmit sent a 1-time activation link to ${ADMIN_PRIMARY_EMAIL}.`);
    console.log(`Check your Gmail inbox/spam and click "Activate Form" once!`);
  }
  console.log(`===============================================`);

  return {
    success: true,
    deliveryChannel: "formsubmit_http",
    status: resultStatus,
    needsActivation,
    recipient: ADMIN_PRIMARY_EMAIL,
    message: needsActivation
      ? `Activation email was sent to ${ADMIN_PRIMARY_EMAIL}. Please click "Activate Form" once in your Gmail inbox or spam folder so future messages drop in automatically!`
      : `Signup alert dispatched to ${ADMIN_PRIMARY_EMAIL}.`,
    gmailWebComposeUrl
  };
}

function saveNotificationLog(entry) {
  try {
    let logs = [];
    if (fs.existsSync(NOTIFICATIONS_FILE)) {
      logs = JSON.parse(fs.readFileSync(NOTIFICATIONS_FILE, "utf-8"));
    }
    logs.unshift(entry); // newest first
    fs.writeFileSync(NOTIFICATIONS_FILE, JSON.stringify(logs.slice(0, 50), null, 2), "utf-8");
  } catch (e) {
    console.error("Failed to write to notification log file:", e.message);
  }
}

function getNotificationLogs() {
  try {
    if (fs.existsSync(NOTIFICATIONS_FILE)) {
      return JSON.parse(fs.readFileSync(NOTIFICATIONS_FILE, "utf-8"));
    }
  } catch (e) {}
  return [];
}

module.exports = {
  sendSignupNotification,
  getNotificationLogs,
  ADMIN_PRIMARY_EMAIL,
  ADMIN_SECONDARY_EMAIL,
};
