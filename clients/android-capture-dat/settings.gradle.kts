import java.util.Properties

pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

val localProperties =
    Properties().apply {
        val path = rootDir.resolve("local.properties")
        if (path.exists()) {
            load(path.inputStream())
        }
    }

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven {
            url = uri("https://maven.pkg.github.com/facebook/meta-wearables-dat-android")
            credentials {
                username = System.getenv("GITHUB_ACTOR") ?: "token"
                password = System.getenv("GITHUB_TOKEN") ?: localProperties.getProperty("github_token", "")
            }
        }
    }
}

rootProject.name = "pedagogyx-capture-dat"
include(":app")
