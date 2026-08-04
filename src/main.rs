use serenity::{
    all::{ClientBuilder, Command, Context, EventHandler, GatewayIntents, Interaction, Message, Ready},
    async_trait,
};
use std::collections::HashMap;

mod commands;
use commands::{all_commands, BotCommand, CommandSource};

const PREFIX: &str = "$";

struct Handler {
    commands: HashMap<&'static str, Box<dyn BotCommand>>,
}

impl Handler {
    fn new() -> Self {
        let commands = all_commands().into_iter().map(|c| (c.name(), c)).collect();
        Self { commands }
    }
}

#[async_trait]
impl EventHandler for Handler {
    async fn ready(&self, ctx: Context, ready: Ready) {
        println!("{} is online and rusty.", ready.user.name);
        let registrations: Vec<_> = self.commands.values().map(|c| c.register()).collect();
        if let Err(e) = Command::set_global_commands(&ctx.http, registrations).await {
            eprintln!("failed to register commands: {e}");
        }
    }

    async fn interaction_create(&self, ctx: Context, interaction: Interaction) {
        if let Interaction::Command(cmd) = interaction {
            if let Some(handler) = self.commands.get(cmd.data.name.as_str()) {
                handler.run(&ctx, &CommandSource::Slash(&cmd), &[]).await;
            }
        }
    }

    async fn message(&self, ctx: Context, msg: Message) {
        if msg.author.bot {
            return;
        }
        let Some(rest) = msg.content.strip_prefix(PREFIX) else { return };
        let mut parts = rest.split_whitespace();
        let Some(name) = parts.next() else { return };
        let args: Vec<String> = parts.map(String::from).collect();

        if let Some(handler) = self.commands.get(name) {
            handler.run(&ctx, &CommandSource::Prefix(&msg), &args).await;
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenvy::dotenv().ok();
    let token: String = dotenvy::var("DISCORD_TOKEN")?;
    let intents = GatewayIntents::GUILD_MESSAGES | GatewayIntents::MESSAGE_CONTENT;

    let mut client = ClientBuilder::new(&token, intents)
        .event_handler(Handler::new())
        .await?;

    client.start().await?;
    Ok(())
}
