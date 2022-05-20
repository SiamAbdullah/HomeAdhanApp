"""A simple class for controlling a Sonos speaker.

    For any given set of arguments to __init__, only one instance of this class
    may be created. Subsequent attempts to create an instance with the same
    arguments will return the previously created instance. This means that all
    SoCo instances created with the same ip address are in fact the *same* SoCo
    instance, reflecting the real world position.

    ..  rubric:: Basic Methods
    ..  autosummary::

        play_from_queue
        play
        play_uri
        pause
        stop
        end_direct_control_session
        seek
        next
        previous
        mute
        volume
        play_mode
        shuffle
        repeat
        cross_fade
        ramp_to_volume
        set_relative_volume
        get_current_track_info
        get_current_media_info
        get_speaker_info
        get_current_transport_info

    ..  rubric:: Queue Management
    ..  autosummary::

        get_queue
        queue_size
        add_to_queue
        add_uri_to_queue
        add_multiple_to_queue
        remove_from_queue
        clear_queue

    ..  rubric:: Group Management
    ..  autosummary::

        group
        partymode
        join
        unjoin
        all_groups
        all_zones
        visible_zones

    ..  rubric:: Player Identity and Settings
    ..  autosummary::

        player_name
        uid
        household_id
        is_visible
        is_bridge
        is_coordinator
        is_soundbar
        is_satellite
        has_satellites
        sub_enabled
        sub_gain
        is_subwoofer
        has_subwoofer
        channel
        bass
        treble
        loudness
        balance
        audio_delay
        night_mode
        dialog_mode
        surround_enabled
        surround_full_volume_enabled
        surround_volume_tv
        surround_volume_music
        soundbar_audio_input_format
        supports_fixed_volume
        fixed_volume
        soundbar_audio_input_format
        soundbar_audio_input_format_code
        trueplay
        status_light
        buttons_enabled
        voice_service_configured
        mic_enabled

    ..  rubric:: Playlists and Favorites
    ..  autosummary::

        get_sonos_playlists
        create_sonos_playlist
        create_sonos_playlist_from_queue
        remove_sonos_playlist
        add_item_to_sonos_playlist
        reorder_sonos_playlist
        clear_sonos_playlist
        move_in_sonos_playlist
        remove_from_sonos_playlist
        get_sonos_playlist_by_attr
        get_favorite_radio_shows
        get_favorite_radio_stations
        get_sonos_favorites

    ..  rubric:: Miscellaneous
    ..  autosummary::

        music_source
        music_source_from_uri
        is_playing_radio
        is_playing_tv
        is_playing_line_in
        switch_to_line_in
        switch_to_tv
        available_actions
        set_sleep_timer
        get_sleep_timer
        create_stereo_pair
        separate_stereo_pair
        get_battery_info
        boot_seqnum

    .. warning::

        Properties on this object are not generally cached and may obtain
        information over the network, so may take longer than expected to set
        or return a value. It may be a good idea for you to cache the value in
        your own code.

    .. note::

        Since all methods/properties on this object will result in an UPnP
        request, they might result in an exception without it being mentioned
        in the Raises section.

        In most cases, the exception will be a
        :class:`soco.exceptions.SoCoUPnPException`
        (if the player returns an UPnP error code), but in special cases
        it might also be another :class:`soco.exceptions.SoCoException`
        or even a `requests` exception.

    """