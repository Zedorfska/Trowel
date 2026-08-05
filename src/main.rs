use serenity::{
    all::{
        ClientBuilder, Command, CommandDataOptionValue, CommandInteraction, Context, EventHandler,
        GatewayIntents, Interaction, Message, Ready,
    },
    async_trait,
};
use std::collections::HashMap;

mod commands;
mod data;

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

fn slash_args(cmd: &CommandInteraction) -> Vec<String> {
    cmd.data
        .options
        .iter()
        .map(|opt| match &opt.value {
            CommandDataOptionValue::String(s) => s.clone(),
            CommandDataOptionValue::Integer(i) => i.to_string(),
            CommandDataOptionValue::Boolean(b) => b.to_string(),
            CommandDataOptionValue::Number(n) => n.to_string(),
            other => format!("{other:?}"),
        })
        .collect()
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
                let args = slash_args(&cmd);
                if let Err(e) = handler.run(&ctx, &CommandSource::Slash(&cmd), &args).await {
                    eprintln!("command '{}' failed: {e}", cmd.data.name);
                }
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
            if let Err(e) = handler.run(&ctx, &CommandSource::Prefix(&msg), &args).await {
                eprintln!("command '{name}' failed: {e}");
            }
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
