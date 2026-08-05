use async_trait::async_trait;
use serenity::all::{CommandInteraction, Context, CreateCommand, Message};

pub enum CommandSource<'a> {
    Slash(&'a CommandInteraction),
    Prefix(&'a Message),
}

impl<'a> CommandSource<'a> {
    pub async fn reply(&self, ctx: &Context, content: impl Into<String>) -> serenity::Result<()> {
        match self {
            CommandSource::Slash(cmd) => {
                use serenity::all::{CreateInteractionResponse, CreateInteractionResponseMessage};
                cmd.create_response(
                    &ctx.http,
                    CreateInteractionResponse::Message(
                        CreateInteractionResponseMessage::new().content(content),
                    ),
                )
                .await
            }
            CommandSource::Prefix(msg) => msg.channel_id.say(&ctx.http, content).await.map(|_| ()),
        }
    }
}

#[async_trait]
pub trait BotCommand: Send + Sync {
    fn name(&self) -> &'static str;
    fn register(&self) -> CreateCommand;
    async fn run(&self, ctx: &Context, source: &CommandSource<'_>, args: &[String]) -> serenity::Result<()>;
}

mod ping;
mod define;

pub fn all_commands() -> Vec<Box<dyn BotCommand>> {
    vec![
        Box::new(ping::Ping),
        Box::new(define::Define)
    ]
}
