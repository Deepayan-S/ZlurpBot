const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const axios = require('axios');
const fs = require('fs');
const qrcode = require('qrcode-terminal');

// WhatsApp client Login session using local auth session (saves login)
const client = new Client({
    authStrategy: new LocalAuth()
});

// Generate QR for login if not already authenticated or local auth deleted from project
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});


// Logs once the bot is ready(after QR scan, phone number login not added)
client.on('ready', () => {
    console.log('✅ WhatsApp bot is ready!');
});

// Listen to incoming WhatsApp messages
client.on('message', async msg => {
    // Check if message contains Instagram reel URL
    if (msg.body.includes("instagram.com/reel/")) {
        msg.reply("⏳ Fetching your reel, please wait...");
        console.log('Received reel URL:', msg.body);

        try {
        // 🔧 REPLACE or UPDATE the API used below if needed
            // This part uses saveig.app API (obiously its not working)
            const apiUrl = 'https://saveig.app/api/ajaxSearch';
              // Send POST request to external API with the reel link
            const response = await axios.post(apiUrl, {
                url: msg.body
            });
            // FOR INTEGRATION:
            // Replace the API above or this entire block with required scraping logic
            // that returns a downloadable video URL

            // Check if response contains reel video data
            if (response.data && response.data.reels && response.data.reels.length > 0) {
                const videoUrl = response.data.reels[0].video;

                console.log('Extracted video URL:', videoUrl);

                // Download the video
                const videoResponse = await axios.get(videoUrl, { responseType: 'arraybuffer' });
                fs.writeFileSync('reel.mp4', videoResponse.data);

                 // Convert to WhatsApp media format and send it back
                const media = MessageMedia.fromFilePath('reel.mp4');
                await client.sendMessage(msg.from, media);

                  // Delete the file after sending
                fs.unlinkSync('reel.mp4');
            } else {
                 // If API does not return, proper response to link sender
                msg.reply("❌ Could not fetch video. Make sure the reel is public and the URL is correct.");
            }
        } catch (error) {
            // Catches error if the request fails or reel is private/invalid
            console.error('Error fetching reel:', error.message);
            msg.reply("❌ Something went wrong while processing your reel.");
        }
    }
});
// Start the WhatsApp client
client.initialize();
