package com.pedagogyx.capture.dat

import android.app.Application
import com.meta.wearable.dat.core.Wearables

class PedagogyXApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        Wearables.initialize(this)
    }
}
