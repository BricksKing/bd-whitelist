# bd-whitelist

A way to make the [BallsDex](https://github.com/Ballsdex-Team/BallsDex-DiscordBot) bot exclusive to specific servers of your choosing. ( my bot is only in one server ;) )

## Installation
Add this to your `config/extra.toml` file
```diff
[[ballsdex.packages]]
location = "git+https://github.com/BricksKing/bd-whitelist.git"
path = "whitelist"
enabled = true
```

## How to use

In the admin panel, click on `Allowed guilds` and add the guilds you want in the whitelist by adding the guild ID, the name is optional. After that, head to `Whitelist setting` click on the boolean, and check Enabled. Alternatively, in Discord, type the slash command `/whitelist enabled:True`
