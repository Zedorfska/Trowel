use super::{BotCommand, CommandSource};
use crate::data::dict::{rijecnik, Rijec};
use async_trait::async_trait;
use serenity::all::{CommandOptionType, Context, CreateCommand, CreateCommandOption};
use strsim::jaro_winkler;

pub struct Define;

const MATCH_THRESHOLD: f64 = 0.85;

fn find_entry<'a>(entries: &'a [Rijec], term: &str) -> Option<&'a Rijec> {
    let term_lower = term.to_lowercase();

    entries
        .iter()
        .filter_map(|entry| {
            let candidates: Vec<&str> = match &entry.keywords {
                Some(kws) if !kws.is_empty() => kws.iter().copied().collect(),
                _ => entry.rijec.into_iter().collect(),
            };

            candidates
                .into_iter()
                .map(|kw| jaro_winkler(&term_lower, &kw.to_lowercase()))
                .fold(None::<f64>, |best, score| Some(best.map_or(score, |b| b.max(score))))
                .map(|score| (entry, score))
        })
        .filter(|(_, score)| *score >= MATCH_THRESHOLD)
        .max_by(|a, b| a.1.total_cmp(&b.1))
        .map(|(entry, _)| entry)
}

#[async_trait]
impl BotCommand for Define {
    fn name(&self) -> &'static str {
        "define"
    }

    fn register(&self) -> CreateCommand {
        CreateCommand::new("define")
            .description("Looks up the definition of a word")
            .add_option(
                CreateCommandOption::new(CommandOptionType::String, "term", "The word to define")
                    .required(true),
            )
    }

    async fn run(&self, ctx: &Context, source: &CommandSource<'_>, args: &[String]) -> serenity::Result<()> {
        let Some(term) = args.first() else {
            return source.reply(ctx, "usage: define <term>").await;
        };

        let entries = rijecnik();
        let entry = find_entry(&entries, term);
        
        let reply = if let Some(r) = entry {
        let mut reply = String::new();

        if let Some(word) = r.display_rijec {
            reply += &format!("# {word}\n");
        }

        if let Some(vrsta) = r.vrsta {
            reply += &format!("-# {vrsta}\n");
        }

        if let Some(defs) = &r.definicija {
            let mut number = 1;
            for d in defs {
                reply += &format!("{number}. {d}\n");
                number += 1;
            }
        } else {
            reply += "Missing definitions!\n";
        }

            reply
        }
        else {
            format!("No entry for '{term}'")
        };

        source.reply(ctx, reply).await
    }
}
