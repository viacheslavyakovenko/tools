package com.vaclav.benchmark.example;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.UUID;

public class ArrayUtil {
    public static byte[] getRandomBytesArray() {

        String randomString = UUID.randomUUID().toString();
        MessageDigest md5 = null;
        try {
            md5 = MessageDigest.getInstance("MD5");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
        md5.update(randomString.getBytes());
        byte[] arrayToSort = md5.digest();
        return arrayToSort;
    }
}