use super::{BotCommand, CommandSource};
use async_trait::async_trait;
use serenity::all::{Context, CreateCommand};

pub struct Ping;

#[async_trait]
impl BotCommand for Ping {
    fn name(&self) -> &'static str {
        "ping"
    }

    fn register(&self) -> CreateCommand {
        CreateCommand::new("ping").description("Replies with pong")
    }

    async fn run(&self, ctx: &Context, source: &CommandSource<'_>, _args: &[String]) -> serenity::Result<()> {
        source.reply(ctx, "pong").await
    }
}
