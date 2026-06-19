import java.io.FileInputStream
import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.pedagogyx.capture.dat"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.pedagogyx.capture.dat"
        minSdk = 29
        targetSdk = 35
        versionCode = 1
        versionName = "0.2.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        // Emulator → host machine API (override in local.properties: pedagogyx.api.base.url)
        val localProps =
            Properties().apply {
                val f = rootProject.file("local.properties")
                if (f.exists()) {
                    load(FileInputStream(f))
                }
            }
        val apiBase =
            localProps.getProperty("pedagogyx.api.base.url")
                ?: "http://10.0.2.2:8080"
        buildConfigField("String", "PEDAGOGYX_API_BASE_URL", "\"$apiBase\"")
        buildConfigField("String", "PEDAGOGYX_SCHOOL_ID", "\"pilot-school-dev\"")
        buildConfigField("String", "PEDAGOGYX_ROOM_ID", "\"room-1\"")
        buildConfigField("String", "PEDAGOGYX_TEACHER_ID", "\"teacher-dev\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        viewBinding = true
        buildConfig = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.mwdat.core)
    implementation(libs.mwdat.camera)
    implementation(libs.mwdat.mockdevice)
    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.okhttp)

    testImplementation(libs.junit)
    testImplementation(libs.okhttp)

    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.espresso.core)
    androidTestImplementation(libs.mwdat.mockdevice)
}
